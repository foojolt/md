


### basic theano
import numpy
import theano.tensor as T
x = T.dscalar('x')
y = T.dscalar('y')
z = x + y
numpy.allclose(z.eval({x : 16.3, y : 12.1}), 28.4)

theano.tensor.vector()
T.dmatrix('y')


### plot
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 10, 1000)
y = np.sin(x)
z = np.cos(x**2)

plt.figure(figsize=(8,4))
plt.plot(x,y,label="$sin(x)$",color="red",linewidth=2)
plt.plot(x,z,"b--",label="$cos(x^2)$")
plt.xlabel("Time(s)")
plt.ylabel("Volt")
plt.title("PyPlot First Example")
plt.ylim(-1.2,1.2)
plt.legend()
plt.show()