import lupa
from lupa import LuaRuntime
lua = LuaRuntime(unpack_returned_tuples=True)

sandbox = lua.require('sandbox')

while True:
	print('Code to run?')
	luacode = input('> ')

	print(sandbox.run(luacode))
