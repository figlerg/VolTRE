set -x
dune exec wordgen -- --regexp "(<g+r<g>_[0,1]>_[0,2])*" --poly 10 --traj 10 
dune exec wordgen -- --regexp "(<r<a*g>_[0,1]>_[0,2])*" --poly 10 --traj 10 

dune exec wordgen -- --regexp "(<g+s<g+r<g>_[0,1]>_[0,2]>_[0,3])*" --poly 10 --traj 10 
dune exec wordgen -- --regexp "(<s<r<a*g>_[0,1]>_[0,2]>_[0,3])*" --poly 10 --traj 10 

dune exec wordgen -- --regexp "(<g+t<g+s<g+r<g>_[0,1]>_[0,2]>_[0,3]>_[0,4])*" --poly 10 --traj 10 
dune exec wordgen -- --regexp "(<t<s<r<a*g>_[0,1]>_[0,2]>_[0,3]>_[0,4])*" --poly 10 --traj 10 

dune exec wordgen -- --regexp "(<g+u<g+t<g+s<g+r<g>_[0,1]>_[0,2]>_[0,3]>_[0,4]>_[0,5])*" --poly 10 --traj 10 
dune exec wordgen -- --regexp "(<u<t<s<r<a*g>_[0,1]>_[0,2]>_[0,3]>_[0,4]>_[0,5])*" --poly 10 --traj 10 

dune exec wordgen -- --regexp "(<g+v<g+u<g+t<g+s<g+r<g>_[0,1]>_[0,2]>_[0,3]>_[0,4]>_[0,5]>_[0,6])*" --poly 10 --traj 10 
dune exec wordgen -- --regexp "(<v<u<t<s<r<a*g>_[0,1]>_[0,2]>_[0,3]>_[0,4]>_[0,5]>_[0,6])*" --poly 10 --traj 10 


dune exec wordgen -- --regexp "(<g+v<g+u<g+t<g+s<g+r<g>_[0,1]>_[0,2]>_[0,3]>_[0,4]>_[0,5]>_[0,6])*" --poly 10 --traj 10 
dune exec wordgen -- --regexp "(<v<u<t<s<r<a*g>_[0,1]>_[0,2]>_[0,3]>_[0,4]>_[0,5]>_[0,6])*" --poly 10 --traj 10 


dune exec wordgen -- --regexp "(<g+w<g+v<g+u<g+t<g+s<g+r<g>_[0,1]>_[0,2]>_[0,3]>_[0,4]>_[0,5]>_[0,6]>_[0,7])*" --poly 10 --traj 10 
dune exec wordgen -- --regexp "(<w<v<u<t<s<r<a*g>_[0,1]>_[0,2]>_[0,3]>_[0,4]>_[0,5]>_[0,6]>_[0,7])*" --poly 10 --traj 10 
