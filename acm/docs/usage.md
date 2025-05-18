# Usage

```
from acm.core import AdaptiveCurvatureMemory
from acm.models import adjust_curvature
from acm.utils import moving_average

acm = AdaptiveCurvatureMemory()
acm.update(adjust_curvature(acm.get_curvature(), 1.1))
print(acm.get_curvature())

# compute the moving average of stored curvatures
print(moving_average(acm.history()))

# reset the memory back to the initial state
acm.reset()
print(acm.history())
```
