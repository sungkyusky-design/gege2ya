extends CharacterBody3D
## 1인칭 플레이어: 걷기, 달리기, 점프, 앉기, 시점 돌리기, 정조준, 총 쏘기
##
## 키는 '물리 키'(키보드 위치)로 읽어요. 그래서 한글 입력 상태여도 WASD가 잘 돼요.

const WALK_SPEED := 5.0
const SPRINT_SPEED := 8.5
const CROUCH_SPEED := 2.5
const AIM_SPEED := 3.0
const JUMP_VELOCITY := 4.8
const KEY_LOOK_SPEED := 2.2        # 화살표 키로 돌리는 빠르기
const MOUSE_SENS := 0.0025         # 마우스 감도
const STAND_EYE := 1.6             # 서 있을 때 눈높이 (미터)
const CROUCH_EYE := 1.0            # 앉았을 때 눈높이
const FIRE_DELAY := 0.1            # 연사 간격 (초)
const SHOT_FORCE := 12.0           # 총알이 상자를 미는 힘
const MAX_HOLES := 60              # 총알 자국 최대 개수

@onready var head: Node3D = $Head
@onready var camera: Camera3D = $Head/Camera3D
@onready var gun: Node3D = $Head/Camera3D/Gun
@onready var flash: OmniLight3D = $Head/Camera3D/Gun/Flash
@onready var ray: RayCast3D = $Head/Camera3D/RayCast3D
@onready var crosshair: Control = get_node_or_null("../HUD/Crosshair")

var gravity: float = ProjectSettings.get_setting("physics/3d/default_gravity")
var crouching := false
var aiming := false
var fire_timer := 0.0
var flash_timer := 0.0
var kick := 0.0                    # 쏘면 1이 되고 점점 0으로 (총이 뒤로 밀리는 정도)
var bob_time := 0.0
var click_queued := false          # 트랙패드를 톡 친 클릭도 놓치지 않게
var gun_hip := Vector3.ZERO        # 허리 자세 총 위치
var holes: Array[Node3D] = []
var hole_mesh := SphereMesh.new()
var spark_mesh := SphereMesh.new()


func _ready() -> void:
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
	ray.add_exception(self)        # 내 몸은 맞히지 않기
	gun_hip = gun.position
	# 총알 자국(검은 점)과 불똥(노란 점) 모양 미리 만들기
	hole_mesh.radius = 0.03
	hole_mesh.height = 0.06
	var hole_mat := StandardMaterial3D.new()
	hole_mat.albedo_color = Color(0.05, 0.05, 0.05)
	hole_mesh.material = hole_mat
	spark_mesh.radius = 0.06
	spark_mesh.height = 0.12
	var spark_mat := StandardMaterial3D.new()
	spark_mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	spark_mat.albedo_color = Color(1.0, 0.85, 0.4)
	spark_mesh.material = spark_mat


func key(code: Key) -> float:
	return 1.0 if Input.is_physical_key_pressed(code) else 0.0


func _unhandled_input(event: InputEvent) -> void:
	# 마우스로 시점 돌리기
	if event is InputEventMouseMotion and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
		rotate_y(-event.relative.x * MOUSE_SENS)
		head.rotate_x(-event.relative.y * MOUSE_SENS)
	if event is InputEventMouseButton and event.pressed:
		Input.mouse_mode = Input.MOUSE_MODE_CAPTURED   # 클릭하면 마우스를 다시 잡아요
		if event.button_index == MOUSE_BUTTON_LEFT:
			click_queued = true
		elif event.button_index == MOUSE_BUTTON_RIGHT:
			aiming = not aiming
	if event is InputEventKey and event.pressed and not event.echo:
		match event.physical_keycode:
			KEY_C:
				crouching = not crouching
			KEY_E:
				aiming = not aiming
			KEY_ESCAPE:
				Input.mouse_mode = Input.MOUSE_MODE_VISIBLE   # 마우스 풀기


func _physics_process(delta: float) -> void:
	# 화살표 키로 시점 돌리기 (마우스 없이도 돼요)
	rotate_y((key(KEY_LEFT) - key(KEY_RIGHT)) * KEY_LOOK_SPEED * delta)
	head.rotate_x((key(KEY_UP) - key(KEY_DOWN)) * KEY_LOOK_SPEED * 0.7 * delta)
	head.rotation.x = clamp(head.rotation.x, deg_to_rad(-85), deg_to_rad(85))

	# 중력과 점프
	if not is_on_floor():
		velocity.y -= gravity * delta
	if key(KEY_SPACE) and is_on_floor():
		velocity.y = JUMP_VELOCITY
		crouching = false

	# 이동: W 앞, S 뒤, A 왼쪽, D 오른쪽
	var sprinting := key(KEY_SHIFT) > 0 and key(KEY_W) > 0 and not crouching and not aiming
	var speed := WALK_SPEED
	if sprinting:
		speed = SPRINT_SPEED
	elif crouching:
		speed = CROUCH_SPEED
	elif aiming:
		speed = AIM_SPEED
	var input := Vector2(key(KEY_D) - key(KEY_A), key(KEY_S) - key(KEY_W))
	var direction := (transform.basis * Vector3(input.x, 0, input.y)).normalized()
	if direction:
		velocity.x = direction.x * speed
		velocity.z = direction.z * speed
	else:
		velocity.x = move_toward(velocity.x, 0, speed)
		velocity.z = move_toward(velocity.z, 0, speed)
	move_and_slide()

	# 앉으면 눈높이가 부드럽게 내려가요
	var eye := CROUCH_EYE if crouching else STAND_EYE
	head.position.y = lerp(head.position.y, eye, 10 * delta)

	# 정조준하면 화면이 확대돼요
	camera.fov = lerp(camera.fov, 55.0 if aiming else 75.0, 12 * delta)
	if crosshair:
		crosshair.visible = not aiming             # 정조준 중엔 총의 빨간 점으로 조준해요

	# 사격: F 키 또는 마우스 왼쪽 (달리는 중엔 못 쏴요)
	fire_timer -= delta
	var fire := key(KEY_F) > 0 or Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT) or click_queued
	click_queued = false
	if fire and fire_timer <= 0 and not sprinting:
		shoot()

	# 총구 불빛은 아주 잠깐만
	flash_timer -= delta
	flash.visible = flash_timer > 0

	update_gun(delta, sprinting)


func update_gun(delta: float, sprinting: bool) -> void:
	# 총 흔들기: 걸으면 흔들리고, 달리면 내리고, 쏘면 뒤로 밀려요
	var moving := Vector2(velocity.x, velocity.z).length() > 0.5 and is_on_floor()
	var target := gun_hip
	if aiming:
		target = Vector3(0, -0.09, -0.3)           # 조준기가 화면 가운데에 오도록 들어 올리기
	if moving:
		bob_time += delta * (14.0 if sprinting else 9.0)
		var size := 0.004 if aiming else 0.014
		target += Vector3(sin(bob_time) * size, -abs(cos(bob_time)) * size, 0)
	else:
		target.y += sin(Time.get_ticks_msec() / 1000.0 * 2.0) * 0.003   # 숨쉬기
	if sprinting:
		target += Vector3(0.06, -0.1, 0.05)
	kick = move_toward(kick, 0.0, delta * 8)
	target.z += kick * 0.06
	gun.position = gun.position.lerp(target, min(1.0, 18 * delta))
	gun.rotation.x = lerp(gun.rotation.x, kick * 0.15 - (0.5 if sprinting else 0.0), min(1.0, 18 * delta))


func shoot() -> void:
	fire_timer = FIRE_DELAY
	kick = 1.0
	flash_timer = 0.05
	head.rotate_x(deg_to_rad(0.5 if aiming else 0.9))   # 반동: 총구가 살짝 올라가요
	ray.force_raycast_update()
	if not ray.is_colliding():
		return
	var target := ray.get_collider() as Node3D
	var point := ray.get_collision_point()
	add_spark(point)
	add_hole(target, point)
	if target is RigidBody3D:                          # 상자는 맞은 방향으로 밀려나요
		var push := -camera.global_basis.z * SHOT_FORCE
		target.apply_impulse(push, point - target.global_position)
	if target.has_method("hit"):
		target.hit()


func add_spark(point: Vector3) -> void:
	var spark := MeshInstance3D.new()
	spark.mesh = spark_mesh
	get_tree().current_scene.add_child(spark)
	spark.global_position = point
	get_tree().create_timer(0.06).timeout.connect(spark.queue_free)


func add_hole(target: Node3D, point: Vector3) -> void:
	# 맞은 물체에 총알 자국을 붙여요 (상자가 날아가면 자국도 같이 움직여요)
	var hole := MeshInstance3D.new()
	hole.mesh = hole_mesh
	target.add_child(hole)
	hole.global_position = point
	holes.append(hole)
	if holes.size() > MAX_HOLES:
		var old: Node3D = holes.pop_front()
		if is_instance_valid(old):
			old.queue_free()
