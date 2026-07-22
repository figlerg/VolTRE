# Figure 2 (fig:cube) — provenance

Figure 2 of the paper has three panels:

- **top left** (`cubecrop3.png`): slices of the hypercube language for n=3 and
  T in {0.5, 1.0, 1.5, 2.0, 2.5}, 10^4 timed words per slice, drawn in 3D.
- **top right** (`outprojsquare.png`): the T=1.5 slice projected on the
  delays (t1, t2), giving the hexagon.
- **bottom**: the volume function V_3(T) of the same language.

## How the original was made

The top panels were produced by Benoit with wordgen + gnuplot. The original
plotting script was not kept; Benoit reconstructed the procedure. wordgen was
called once per duration (regexp `<a>_[0,1]*`, poly 3, 10^4 exact-duration
trajectories), each writing a `.dat` of 3 event delays per line:

```
wordgen --poly 3 --regexp "<a>_[0,1]*" --traj 10000 --exact-duration --expected-duration 0.50001 out05.dat
wordgen --poly 3 --regexp "<a>_[0,1]*" --traj 10000 --exact-duration --expected-duration 1.00001 out10.dat
wordgen --poly 3 --regexp "<a>_[0,1]*" --traj 10000 --exact-duration --expected-duration 1.50001 out15.dat
wordgen --poly 3 --regexp "<a>_[0,1]*" --traj 10000 --exact-duration --expected-duration 2.00001 out20.dat
wordgen --poly 3 --regexp "<a>_[0,1]*" --traj 10000 --exact-duration --expected-duration 2.50001 out25.dat
gnuplot gnuplot4_3d.gnu
```

The `.dat` files here are Benoit's committed data (data of record for fast
mode). `gnuplot4_3d_benoit_original.gnu` is his original 3D script, kept for
reference; it needs a `cube.txt` wireframe that was not in his archive, so we
regenerated `cube.txt` (the 12 edges of the unit cube).

## What the artifact does

`make_cube_fig.py` reproduces all three panels:

- 3D cube and projection: gnuplot, using `cube_3d.gnu` / `cube_projection.gnu`
  (parametrized versions of Benoit's script).
- Volume function: computed by VolTRE itself (`slice_volume` on the hypercube
  spec, n=3), which is exactly the function the paper plots.

Fast mode uses the committed `data/*.dat`. Full mode (`--resample`)
regenerates the `.dat` with wordgen, using Benoit's commands above.
