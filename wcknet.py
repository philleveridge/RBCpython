#BY Andrey K from youtube
#
import math
import random

from graphviz import Digraph

def trace(root):
    nodes, edges = set(), set()
    def build(v):
        if v not in nodes:
            nodes.add(v)
            for child in v._prev:
                edges.add((child, v))
                build(child)
    build(root)
    return nodes, edges

def draw_dot(root, format='svg', rankdir='LR'):
    """
    format: png | svg | ...
    rankdir: TB (top to bottom graph) | LR (left to right)
    """
    assert rankdir in ['LR', 'TB']
    nodes, edges = trace(root)
    dot = Digraph(format=format, graph_attr={'rankdir': rankdir}) #, node_attr={'rankdir': 'TB'})
    
    for n in nodes:
        uid = str(id(n))
        dot.node(name=uid, label = "{ %s | data %.4f | grad %.4f }" % (n.label, n.data, n.grad), shape='record')
        if n._op:
            dot.node(name=str(id(n)) + n._op, label=n._op)
            dot.edge(uid + n._op, uid)
    
    for n1, n2 in edges:
        dot.edge(str(id(n1)), str(id(n2)) + n2._op)
    
    return dot


  

class Value:
    def __init__(self,data, _children=(), _op='', label=''):
        self.data=data
        self.grad=0.0
        self._backward = lambda: None
        self._prev = set(_children)
        self._op = _op
        self.label = label
        
    def __neg__(self) :
        return self * -1
    
    def __sub__ (self,other) :
        return self + (-other)
        
    def __repr__(self):
        return f"Value(data={self.data})"
    
    def __add__(self,other):
        other = other if isinstance(other,Value) else Value(other)
        out = Value(self.data + other.data, (self, other), '+')
        def _backward():
            self.grad += 1.0 * out.grad
            other.grad += 1.0 * out.grad
        out._backward = _backward
        return out
    
    def __mul__(self,other):
        other = other if isinstance(other,Value) else Value(other)
        out = Value(self.data * other.data, (self, other), '*')
        def _backward():
            self.grad += other.data*out.grad
            other.grad += self.data*out.grad
        out._backward = _backward
        return out
    
    def __rmul__(self,other):
        return self * other
    
    def __radd__(self,other):
        return self + other
    
    def __rsub__(self,other):
        return other + (-self)
    
    def __truediv__(self,other):
        return self * other**-1
    
    def __rtruediv__(self,other):
        return other * self**-1
    
    def __pow__(self,other):
        assert isinstance(other, (int,float)), " only float or int"
        out = Value(self.data**other, (self,), f'**{other}')
        
        def _backward():
            self.grad += other * (self.data ** (other -1)) * out.grad # tbd
        
        out._backward= _backward
        return out
    
    def tanh(self):
        x=self.data
        t = (math.exp(2*x)-1)/(math.exp(2*x)+1)
        out = Value(t, (self,), 'tanh')
        def _backward():
            self.grad += (1-t**2) * out.grad
        out._backward = _backward
        return out
    
    def relu(self):
        out = Value(0 if self.data<0 else self.data, (self,), 'Relu')
        
        def _backward():
            self.grad += (out.data >0) * out.grad
        out._backward = _backward
         
        return out
    
    def exp(self):
        x=self.data
        out = Value(math.exp(x), (self,), 'exp')
        def _backward():
            self.grad += out.data * out.data
        out._backward = _backward
        return out
    
    def backward(self) :
        topo = []
        visited = set()
        def build_topo(v):
            if v not in visited:
                for child in v._prev:
                    build_topo(child)
                topo.append(v)
        build_topo(self)
        self.grad=1.0
        for node in reversed(topo):
            node._backward()


class Module:
    def zero_grad(self):
        for p in self.parameters():
            p.grad=0
    def parameters(self):
        return []
    

class Neuron(Module):
    def __init__(self,nin):
        self.w = [Value(random.uniform(-1,1)) for _ in range(nin)]
        self.b = Value(random.uniform(-1,1))
                       
    def __call__(self,x):
        #print (list(zip(self.w,x)))
        act = sum((wi*xi for wi,xi in zip(self.w, x)), self.b)
        out = act.tanh()
        return out
    
    def parameters(self):
        return self.w + [self.b]
    
class Layer:
    def __init__(self,nin,nout):
        self.neurons = [Neuron(nin) for _ in range(nout)]
        
    def __call__(self,x):
        outs = [n(x) for n in self.neurons]
        return outs[0] if len(outs)==1 else outs
    
    def parameters(self):
        return [p for neuron in self.neurons for p in neuron.parameters()]
                       
class MLP:
    def __init__(self,nin,nouts):
        sz = [nin] + nouts
        self.layers = [Layer(sz[i],sz[i+1]) for i in range(len(nouts))]
        
    def __call__(self,x):
        for layer in self.layers:
            x=layer(x)
        return x
    def parameters(self):
        return [p for layer in self.layers for p in layer.parameters()]
                       

def test(id=50):
	print("MLP test")

	x  = [2.0,3.0, -1.0]
	n  = MLP(3, [4,4,1])
	xs = [ [2.0,3.0,-1.0], [3.0,-1.0,0.5], [0.5,1.0,1.0], [1.0,1.0,-1.0],]
	ys = [1.0,-1.0,-1.0,1.0]
	y  = []

	for i in range(id):
		yp = [n(x) for x in xs]		
		loss=[(y-x)**2 for x,y in zip(ys,yp)]
		loss=sum(loss)

		print (i, 'loss=',loss)
		
		for p in n.parameters():
		    p.grad = 0.0

		loss.backward()
		#print (n.layers[0].neurons[0].w[0], n.layers[0].neurons[0].w[0].grad)

		for p in n.parameters():
		    p.data += -0.05 * p.grad


	print('final=', yp)

import sys
if __name__ == "__main__":
    if len(sys.argv)>1 :
        test(int(sys.argv[1]))

    else :
        test()

