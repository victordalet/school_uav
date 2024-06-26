# school_uav

---

## 1. Create the environment

---


You can use this web site to draw the environement like this https://jspaint.app/
- draw ways in black
- draw start in red
- draw classes in green
- draw in the first line in blue the estimated 1 meter (to obtain a good speed of the drone)

![map.png](assets/map.png)

## 2. Counting mission

---

```
export PYTHONPATH=$PYTHONPATH:$(pwd)
python src/run.py count {map.png}
```

## 3. Reconnaissance mission

---

```
export PYTHONPATH=$PYTHONPATH:$(pwd)
python src/run.py reco {map.png}
```