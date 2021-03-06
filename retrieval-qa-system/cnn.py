from utils import sample_weights, sigmoid, tanh, relu

import theano
import theano.tensor as T


def layers(x, window, dim_emb, dim_hidden, n_layers, activation=tanh):
    params = []
    zero = T.zeros((1, 1, dim_emb * window), dtype=theano.config.floatX)

    def zero_pad_gate(matrix):
        return T.neq(T.sum(T.eq(matrix, zero), 2, keepdims=True), dim_emb * window)

    for i in xrange(n_layers):
        if i == 0:
            W = theano.shared(sample_weights(dim_emb * window, dim_hidden))
            h = T.max(zero_pad_gate(x) * relu(T.dot(x, W)), 1)
#            h = T.max(T.dot(x, W), 1)
        else:
            W = theano.shared(sample_weights(dim_hidden, dim_hidden))
            h = activation(T.dot(h, W))
        params.append(W)

    return h, params


