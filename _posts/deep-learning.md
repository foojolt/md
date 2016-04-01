---
title: deep learning essentials
date: 2016-03-28 11:07:14
tags:
 - deep-learning
---

### deep-learning

[deeplearning-tutorial](http://deeplearning.net/tutorial/)

    Very Brief Introduction to Machine Learning for AI


[free books](http://greenteapress.com/wp/)
think stat, think python

### milestone

    
    Unsupervised Feature Learning and Deep Learning.
http://ufldl.stanford.edu/wiki/index.php/
https://github.com/ty4z2008/Qix/blob/master/dl.md
neuron
autoencoder: using theano to implement it

    Theano

    五子棋

    五子棋 powered by deeplearning

    deeplearning for NLP

    optinal
https://github.com/ty4z2008/Qix/blob/master/dl.md   

### numpy
narray, multidimensional array object
sudo apt-get build-dep python-scipy

    import numpy
    import theano.tensor as T
    x = T.dscalar('x')
    y = T.dscalar('y')
    z = x + y
    numpy.allclose(z.eval({x : 16.3, y : 12.1}), 28.4)

    import theano
    a = theano.tensor.vector() # declare variable
    out = a + a ** 10               # build symbolic expression
    f = theano.function([a], out)   # compile function
    print(f([0, 1, 2]))

    from theano import shared
    state = shared(0)
    inc = T.iscalar('inc')
    accumulator = function([inc], state, updates=[(state, state+inc)])

from theano.tensor.shared_randomstreams import RandomStreams
from theano import function
srng = RandomStreams(seed=234)
rv_u = srng.uniform((2,2))
rv_n = srng.normal((2,2))
f = function([], rv_u)
g = function([], rv_n, no_default_updates=True)    #Not updating rv_n.rng
nearly_zeros = function([], rv_u + rv_u - 2 * rv_u)

