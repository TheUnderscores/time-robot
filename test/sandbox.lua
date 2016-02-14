local sandbox = {}

if _VERSION ~= 'Lua 5.1' then
	print('WARN: Sandbox is designed for Lua 5.1')
end

local safeEnv = {
	assert = assert,
	error = error,
	ipairs = ipairs,
	next = next,
	pairs = pairs,
	pcall = pcall,
	print = print,	-- WARN: This prints to stdout.
	select = select,
	tonumber = tonumber,
	tostring = tostring,
	type = type,
	unpack = unpack,
	_VERSION = _VERSION,
	xpcall = xpcall,
	coroutine = {
		create = coroutine.create,
		resume = coroutine.resume,
		running = coroutine.running,
		status = coroutine.status,
		wrap = coroutine.wrap,
		yield = coroutine.yield,	-- WARN: Probably safe, assuming caller handles it.
	},
	string = {
		byte = string.byte,
		char = string.char,
		find = string.find,
		format = string.format,
		gmatch = string.gmatch,
		gsub = string.gsub,
		len = string.len,
		lower = string.lower,
		match = string.match,
		rep = string.rep,
		reverse = string.reverse,
		sub = string.sub,
		upper = string.upper,
	},
	table = {
		insert = table.insert,
		maxn = table.maxn,
		remove = table.remove,
		sort = table.sort,
	},
	math = {
		abs = math.abs,
		acos = math.acos,
		asin = math.asin,
		atan = math.atan,
		atan2 = math.atan2,
		ceil = math.ceil,
		cos = math.cos,
		cosh = math.cosh,
		deg = math.deg,
		exp = math.exp,
		floor = math.floor,
		fmod = math.fmod,
		frexp = math.frexp,
		huge = math.huge,
		ldexp = math.ldexp,
		log = math.log,
		log10 = math.log10,
		max = math.max,
		min = math.min,
		modf = math.modf,
		pi = math.pi,
		pow = math.pow,
		rad = math.rad,
		random = math.random,	-- WARN: Not 100% safe.
		sin = math.sin,
		sinh = math.sinh,
		sqrt = math.sqrt,
		tan = math.tan,
		tanh = math.tanh,
	},
	os = {
		clock = os.clock,
		difftime = os.difftime,
		time = os.time,
	},
}
safeEnv._G = safeEnv	-- Sets _G to the safe environment.

function sandbox.run(unsafeCode)
	if unsafeCode:byte(1) == 27 then
		-- This is binary bytecode.
		return nil, 'Binary bytecode is disallowed.'
	end
	local unsafeFunction, msg = loadstring(unsafeCode)
	if not unsafeFunction then
		return nil, msg
	end
	setfenv(unsafeFunction, safeEnv)
	return pcall(unsafeFunction)
end

function sandbox.add(tableToAdd)
	for key, value in pairs(tableToAdd) do
		safeEnv[key] = value
	end
end

return sandbox