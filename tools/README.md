# TOOLS

---

## 1. Show depth estimation

---

```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)
python tools/show_depth_estimation.py {number_separation_frame}
```

## 2. Display map

---

```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)
python tools/display_map.py {path.png}
```

## 3. Display counting student

---

```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)
python tools/number_student.py
```

## 4. Display learning student

---

```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)
python tools/learn_student.py {image_test.png}
```