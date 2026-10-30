extends CharacterBody3D
## 적 병사: 돌아다니다가 플레이어를 보면 쫓아와서 쏴요.
## 몸통은 3발, 머리는 1발이면 쓰러져요.

const WALK_SPEED := 1.6            # 돌아다닐 때
const RUN_SPEED := 3.4             # 쫓아올 때
const SIGHT_RANGE := 32.0          # 이 거리 안이고 가리는 게 없으면 나를 봐요
const SHOOT_RANGE := 22.0
const KEEP_DISTANCE := 9.0         # 이 정도 거리까지만 다가와요
const FIRE_DELAY := 1.2
const DAMAGE := 7
const VIEW_ANGLE := 65.0           # 앞쪽 이 각도 안에 있어야 나를 봐요 (뒤로 몰래 다가갈 수 있어요)
const HEAD_HEIGHT := 1.48          # 이보다 위를 맞으면 헤드샷
const BODY_DAMAGE := 34
const HEAD_DAMAGE := 100

var hp := 100
var dead := false
var player: Node3D
var gravity: float = ProjectSettings.get_setting("physics/3d/default_gravity")
var fire_timer := randf_range(1.5, 2.5)   # 처음엔 바로 쏘지 않아요
var step_timer := 0.0
var wander_dir := Vector3.ZERO
var wander_timer := 0.0
var hurt_timer := 0.0
var sees_player := false
var alerted := false               # 한 번 나를 보거나 맞으면 계속 찾아요
var hurt_mat := StandardMaterial3D.new()

@onready var eyes: Node3D = $Eyes
@onready var flash: OmniLight3D = $Gun/Flash
@onready var meshes: Array[MeshInstance3D] = [$Legs, $Body, $Head, $Helmet, $Gun/Mesh]


func _ready() -> void:
	add_to_group("enemies")
	player = get_tree().get_first_node_in_group("player")
	hurt_mat.albedo_color = Color(0.8, 0.05, 0.05)


func _physics_process(delta: float) -> void:
	if not is_on_floor():
		velocity.y -= gravity * delta
	if dead:
		velocity.x = 0
		velocity.z = 0
		move_and_slide()
		return

	hurt_timer -= delta
	if hurt_timer <= 0:
		for m in meshes:
			m.material_override = null        # 붉게 번쩍인 뒤 원래 색으로
	flash.visible = false

	var to_player := player.global_position - global_position
	to_player.y = 0
	var distance := to_player.length()
	var forward := -global_basis.z
	var in_view := alerted or rad_to_deg(forward.angle_to(to_player)) < VIEW_ANGLE
	sees_player = distance < SIGHT_RANGE and in_view and can_see_player()
	if sees_player:
		alerted = true

	var move := Vector3.ZERO
	var speed := WALK_SPEED
	if sees_player and not player.dead:
		face(to_player, delta)
		if distance > KEEP_DISTANCE:
			move = to_player.normalized()
			speed = RUN_SPEED
		fire_timer -= delta
		if fire_timer <= 0 and distance < SHOOT_RANGE:
			shoot(distance)
	else:
		wander_timer -= delta
		if wander_timer <= 0 or is_on_wall():
			wander_timer = randf_range(2.0, 4.0)
			var angle := randf() * TAU
			wander_dir = Vector3(sin(angle), 0, cos(angle)) if randf() < 0.7 else Vector3.ZERO
		move = wander_dir
		if move:
			face(move, delta)

	velocity.x = move.x * speed
	velocity.z = move.z * speed
	move_and_slide()

	# 발소리: 무거운 군화 소리. 소리가 나는 방향에서 들려요
	if move and is_on_floor():
		step_timer -= delta * speed / WALK_SPEED * 0.6
		if step_timer <= 0:
			step_timer = 0.5
			Sfx.play_at(get_parent(), "step_enemy", global_position, -2.0)


func face(direction: Vector3, delta: float) -> void:
	var target_angle := atan2(-direction.x, -direction.z)
	rotation.y = lerp_angle(rotation.y, target_angle, min(1.0, 8 * delta))


func can_see_player() -> bool:
	var space := get_world_3d().direct_space_state
	var target: Vector3 = player.get_node("Head").global_position
	var query := PhysicsRayQueryParameters3D.create(eyes.global_position, target)
	query.exclude = [get_rid()]
	var hit := space.intersect_ray(query)
	return hit and hit.collider == player


func shoot(distance: float) -> void:
	fire_timer = FIRE_DELAY * randf_range(0.7, 1.3)
	flash.visible = true
	Sfx.play_at(get_parent(), "enemy_rifle", flash.global_position)
	# 멀수록, 내가 달리거나 앉아 있으면 덜 맞아요
	var chance := 0.45 - distance / SHOOT_RANGE * 0.25
	if player.crouching:
		chance *= 0.7
	if Vector2(player.velocity.x, player.velocity.z).length() > 6.0:
		chance *= 0.6
	if randf() < chance:
		player.take_damage(DAMAGE, global_position)


## 총에 맞았을 때. 돌려주는 값: "hit" 맞힘, "kill" 쓰러뜨림, "headshot" 머리로 쓰러뜨림
func take_hit(point: Vector3, direction: Vector3) -> String:
	if dead:
		return ""
	var headshot := point.y - global_position.y > HEAD_HEIGHT
	hp -= HEAD_DAMAGE if headshot else BODY_DAMAGE
	Blood.spray(get_parent(), point, direction, 60 if headshot else 30)
	for m in meshes:
		m.material_override = hurt_mat         # 맞으면 붉게 번쩍
	hurt_timer = 0.08
	# 맞으면 나를 알아채고 돌아봐요
	alerted = true
	fire_timer = max(fire_timer, 0.4)
	face(-direction, 1.0)
	if hp <= 0:
		die(direction)
		return "headshot" if headshot else "kill"
	return "hit"


func die(direction: Vector3) -> void:
	dead = true
	$CollisionShape3D.set_deferred("disabled", true)    # 시체는 총알이 지나가요
	for m in meshes:
		m.material_override = null
	# 맞은 방향으로 뒤로 넘어져요
	face(-direction, 1.0)
	var tween := create_tween()
	tween.tween_property(self, "rotation:x", PI / 2, 0.45).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
	tween.parallel().tween_property(self, "position", position + direction * 0.6, 0.45)
	# 쓰러진 자리에 피 웅덩이가 점점 퍼져요
	var pool := Blood.splat(get_parent(), global_position + direction * 0.9 + Vector3.UP * 0.01, Vector3.UP, 0.1)
	var pool_tween := pool.create_tween()
	pool_tween.tween_property(pool, "scale", Vector3(9, 1, 9), 3.0).set_delay(0.4)
	# 15초 뒤 사라져요
	get_tree().create_timer(15.0).timeout.connect(queue_free)
