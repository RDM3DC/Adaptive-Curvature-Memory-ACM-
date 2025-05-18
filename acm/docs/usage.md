# Usage

```
from acm.core import AdaptiveCurvatureMemory
from acm.models import adjust_curvature

acm = AdaptiveCurvatureMemory()
acm.update(adjust_curvature(acm.get_curvature(), 1.1))
print(acm.get_curvature())

# reset memory back to a single initial value
acm.reset()
```
