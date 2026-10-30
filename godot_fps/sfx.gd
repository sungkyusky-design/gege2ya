class_name Sfx
## 효과음을 코드로 만들어요 (소리 파일이 필요 없어요).
## 처음 쓸 때 한 번 만들어 두고 다음부터는 그대로 다시 써요.

const RATE := 22050

# 이름: [길이(초), 줄어드는 빠르기, 잡음 양, 부드럽게(0~1), 쿵 소리 높이(Hz), 쿵 양, 맑은 소리 높이(Hz), 맑은 소리 양]
const RECIPES := {
	"rifle":       [0.30, 16.0, 1.0, 0.25, 85.0, 0.9, 0.0, 0.0],
	"enemy_rifle": [0.35, 13.0, 1.0, 0.55, 65.0, 1.0, 0.0, 0.0],
	# 내 발소리: 가볍고 짧은 '톡'
	"step_player": [0.06, 70.0, 0.6, 0.45, 170.0, 0.35, 0.0, 0.0],
	# 적 발소리: 무거운 군화 '쿵' + 장비가 부딪히는 '찰칵'
	"step_enemy":  [0.16, 30.0, 0.9, 0.8, 62.0, 1.0, 2600.0, 0.12],
	"hit":         [0.10, 35.0, 0.7, 0.75, 110.0, 1.0, 0.0, 0.0],
	"headshot":    [0.25, 18.0, 0.2, 0.2, 0.0, 0.0, 1900.0, 0.7],
	"hurt":        [0.25, 14.0, 0.5, 0.85, 55.0, 1.0, 0.0, 0.0],
}

static var _cache := {}


static func stream(sound: String) -> AudioStreamWAV:
	if _cache.has(sound):
		return _cache[sound]
	var r: Array = RECIPES[sound]
	var count := int(RATE * r[0])
	var data := PackedByteArray()
	data.resize(count * 2)
	var rng := RandomNumberGenerator.new()
	rng.seed = sound.hash()
	var smooth := 0.0
	for i in count:
		var t := float(i) / RATE
		var envelope := exp(-t * r[1])
		smooth = lerp(rng.randf_range(-1.0, 1.0), smooth, r[3])
		var sample: float = smooth * r[2] + sin(TAU * r[4] * t) * r[5] + sin(TAU * r[6] * t) * r[7]
		sample = clamp(sample * envelope * 0.6, -1.0, 1.0)
		data.encode_s16(i * 2, int(sample * 32767))
	var wav := AudioStreamWAV.new()
	wav.format = AudioStreamWAV.FORMAT_16_BITS
	wav.mix_rate = RATE
	wav.data = data
	_cache[sound] = wav
	return wav


## 내 소리 (어디서나 같은 크기로 들려요)
static func play(parent: Node, sound: String, volume_db := 0.0) -> void:
	var player := AudioStreamPlayer.new()
	player.stream = stream(sound)
	player.volume_db = volume_db
	player.pitch_scale = randf_range(0.92, 1.08)      # 매번 살짝 다르게
	parent.add_child(player)
	player.play()
	player.finished.connect(player.queue_free)


## 주변 소리 (멀면 작게, 왼쪽에서 나면 왼쪽에서 들려요)
static func play_at(parent: Node, sound: String, pos: Vector3, volume_db := 0.0) -> void:
	var player := AudioStreamPlayer3D.new()
	player.stream = stream(sound)
	player.volume_db = volume_db
	player.unit_size = 5.0
	player.max_distance = 45.0
	player.pitch_scale = randf_range(0.92, 1.08)
	parent.add_child(player)
	player.global_position = pos
	player.play()
	player.finished.connect(player.queue_free)
