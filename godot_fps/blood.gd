class_name Blood
## 피 효과: 튀는 핏방울, 벽과 바닥에 남는 핏자국, 쓰러진 적 밑의 피 웅덩이

const MAX_SPLATS := 40

static var _drop_mesh: SphereMesh
static var _splat_mat: StandardMaterial3D
static var _splats: Array[Node3D] = []


static func _setup() -> void:
	if _drop_mesh:
		return
	var drop_mat := StandardMaterial3D.new()
	drop_mat.albedo_color = Color(0.32, 0.0, 0.0)
	drop_mat.roughness = 0.6
	_drop_mesh = SphereMesh.new()
	_drop_mesh.radius = 0.018
	_drop_mesh.height = 0.036
	_drop_mesh.material = drop_mat
	_splat_mat = StandardMaterial3D.new()
	_splat_mat.albedo_color = Color(0.22, 0.0, 0.0)
	_splat_mat.roughness = 0.35                   # 젖어서 살짝 반짝여요
	_splat_mat.metallic_specular = 0.2


## 맞은 자리에서 핏방울이 튀고, 총알이 지나간 뒤쪽 벽·바닥에 핏자국이 남아요
static func spray(parent: Node, point: Vector3, direction: Vector3, amount: int) -> void:
	_setup()
	var drops := CPUParticles3D.new()
	drops.mesh = _drop_mesh
	drops.one_shot = true
	drops.explosiveness = 1.0
	drops.amount = amount
	drops.lifetime = 0.5
	drops.direction = (-direction * 0.5 + Vector3.UP * 0.5).normalized()   # 맞은 쪽(내 쪽)과 위로 튀어요
	drops.spread = 50.0
	drops.initial_velocity_min = 2.0
	drops.initial_velocity_max = 5.5
	drops.scale_amount_min = 0.6
	drops.scale_amount_max = 2.0
	parent.add_child(drops)
	drops.global_position = point
	drops.restart()                               # 바로 한 번 뿜어내기
	drops.get_tree().create_timer(1.5).timeout.connect(drops.queue_free)
	# 총알이 지나간 뒤쪽 벽이나 바닥에 핏자국
	var space := drops.get_world_3d().direct_space_state
	for target in [point + direction * 3.0, point + Vector3.DOWN * 3.0]:
		var query := PhysicsRayQueryParameters3D.create(point, target)
		query.collide_with_bodies = true
		var hit := space.intersect_ray(query)
		if hit and hit.collider is StaticBody3D:
			splat(parent, hit.position, hit.normal, randf_range(0.15, 0.3))
			break


## 표면에 납작한 핏자국을 붙여요
static func splat(parent: Node, pos: Vector3, normal: Vector3, radius: float) -> MeshInstance3D:
	_setup()
	var mesh := CylinderMesh.new()
	mesh.top_radius = radius
	mesh.bottom_radius = radius
	mesh.height = 0.004
	mesh.radial_segments = 16
	mesh.material = _splat_mat
	var spot := MeshInstance3D.new()
	spot.mesh = mesh
	parent.add_child(spot)
	spot.global_position = pos + normal * 0.004
	if not normal.is_equal_approx(Vector3.UP):
		spot.quaternion = Quaternion(Vector3.UP, normal.normalized())   # 표면 방향에 맞춰 눕히기
	spot.scale = Vector3(randf_range(0.8, 1.3), 1, randf_range(0.8, 1.3))
	_splats.append(spot)
	if _splats.size() > MAX_SPLATS:
		var old: Node3D = _splats.pop_front()
		if is_instance_valid(old):
			old.queue_free()
	return spot
