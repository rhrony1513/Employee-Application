# Deploy hpa
kubectl autoscale deployment myapp --cpu-percent=50 --min=1 --max=10 -n final

# Generate load
kubectl run -i --tty load-generator --rm --image=busybox:1.28 --restart=Never -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://localhost:81; done"

# Monitor hpa
kubectl get hpa myapp -n final --watch 
kubectl get pod -n final --watch 
