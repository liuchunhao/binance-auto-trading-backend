import sys
import os
sys.path.append('src')

print(sys.path)
print(os.path.abspath('.'))

from common.datetime import render_epoch_time
print(render_epoch_time(1111111111))


from src.config import TOKEN
print(TOKEN)

