import math


def str_sum(*array, sep=''):
    return sep.join(str(a) for a in array)


def to_node(b):
    return b if isinstance(b, __node) else const(b)


class __node:
    def __init__(self, name="none_name", *parents, value=0.0) -> None:
        self.p: list['__node'] = [*parents]
        self.name = name
        self.v = value

    def diff(self, param_name) -> '__node':
        return const(float(param_name == self.name))

    def get_value(self):
        return self.v

    def __str__(self) -> str:
        return str(self.name)

    def __lshift__(self, n: '__node'):
        self.p.append(n)
        return self

    def __rshift__(self, n: '__node'):
        n.p.append(self)
        return n

    def __add__(self, b: '__node') -> '__node':
        return add(self, to_node(b))

    def __radd__(self, b: '__node') -> '__node':
        return add(to_node(b), self)

    def __rsub__(self, b: '__node') -> '__node':
        return add(to_node(b), -(self))

    def __sub__(self, b: '__node') -> '__node':
        return add(self, -(to_node(b)))

    def __mul__(self, b: '__node') -> '__node':
        return mul(self, to_node(b))

    def __rmul__(self, b: '__node') -> '__node':
        return mul(to_node(b), self)

    def __truediv__(self, b: '__node') -> '__node':
        return mul(self, reverse(to_node(b)))

    def __rtruediv__(self, b: '__node') -> '__node':
        return mul(reverse(self), to_node(b))

    def __neg__(self) -> '__node':
        return negative(self)

    def __pow__(self, b: int):
        return pow_node(self, b)

    def __eq__(self, b: '__node') -> bool:
        if type(self) == type(b) and self.name == b.name and self.v == b.v:
            if not (j := (len(b.p) == len(self.p))):
                return False
            i = 0
            while i < len(self.p) and (j := (j and (self.p[i] is b.p[i]))):
                i += 1
            return j or self.p == b.p
        else:
            return False

    def __ne__(self, b: '__node') -> bool:
        return not (self == b)

    def get_optim_p(self):
        k = [p.optim() for p in self.p]
        while None in k:
            k.remove(None)
        return k

    def optim(self):
        self.p = self.get_optim_p()
        return self

    def get_deep(self) -> list[list['__node']]:
        dd = {}
        self.__deep__(dd)
        l = [[] for _ in range(max(dd.keys()) if dd else 0)]
        for i in range(len(dd)):
            l[i] = dd[i + 1]
            h = []
            for j in l[i]:
                if not sum([i is j for i in h]):
                    h.append(j)
            l[i] = h
        return l

    def __deep__(self, deep_dict):
        deep = max((p.__deep__(deep_dict) for p in self.p), default=0) + 1
        if deep in deep_dict:
            deep_dict[deep].append(self)
        else:
            deep_dict[deep] = [self]
        return deep

    def update_value(self):
        pass

    def replace_is_parent_nodes(self, old, new):
        k = []
        for p in self.p:
            if p is old:
                k.append(new)
            else:
                k.append(p)
        self.p = k
        for p in self.p:
            p.replace_is_parent_node(old, new)

    def replace_eq_parent_nodes(self, old, new):
        k = []
        for p in self.p:
            if p == old:
                k.append(new)
            else:
                k.append(p)
        self.p = k
        for p in self.p:
            p.replace_eq_parent_nodes(old, new)

    def replace_eq_parent_node(self, new):
        k = []
        for p in self.p:
            if (not p is new) and p == new:
                k.append(new)
            else:
                k.append(p)
        self.p = k
        for p in self.p:
            p.replace_eq_parent_node(new)


class variable(__node):
    def __init__(self, name="none_name", value=0) -> None:
        super().__init__(name=name, value=value)

    def __deep__(self, deep_dict):
        if 1 in deep_dict:
            deep_dict[1].append(self)
        else:
            deep_dict[1] = [self]
        return 1


class const(variable):
    def __init__(self, value=0) -> None:
        super().__init__(name='const', value=value)

    def __add__(self, b: '__node') -> '__node':
        if type(b) != const:
            return super().__add__(b)
        else:
            return const(self.v + b.v)

    def __radd__(self, b: '__node') -> '__node':
        if type(b) != const:
            return super().__radd__(b)
        else:
            return const(self.v + b.v)

    def __mul__(self, b: '__node') -> '__node':
        if type(b) != const:
            return super().__mul__(b)
        else:
            return const(self.v * b.v)

    def __rmul__(self, b: '__node') -> '__node':
        if type(b) != const:
            return super().__rmul__(b)
        else:
            return const(self.v * b.v)

    def __sub__(self, b: '__node') -> '__node':
        if type(b) != const:
            return super().__sub__(b)
        else:
            return const(self.v - b.v)

    def __rsub__(self, b: '__node') -> '__node':
        if type(b) != const:
            return super().__rsub__(b)
        else:
            return const(b.v - self.v)

    def __str__(self) -> str:
        return str(self.v)

    def __neg__(self) -> '__node':
        return const(-self.v)

    def __truediv__(self, b: '__node') -> '__node':
        if type(b) != const:
            return super().__truediv__(b)
        else:
            return const(self.v/self.b)

    def __rtruediv__(self, b: '__node') -> '__node':
        if type(b) != const:
            return super().__rtruediv__(b)
        else:
            return const(b.v/self.v)

    def __eq__(self, b: '__node') -> bool:
        return type(self) == type(b) and self.v == b.v


class add(__node):
    def __init__(self, *parents) -> None:
        super().__init__("add_node", *parents)

    def diff(self, param_name) -> 'add':
        return add(*[n.diff(param_name) for n in self.p])

    def get_value(self):
        return sum(i.get_value() for i in self.p)

    def update_value(self):
        self.v = sum(i.v for i in self.p)

    def __str__(self) -> str:
        if len(self.p) == 0:
            return "0"
        return f"({str_sum(*self.p, sep='+')})"

    def __add__(self, b: '__node'):
        return add(*self.p, to_node(b))

    def __optim_local_func__(self):
        for p in self.p:
            f = 0
            h = []
            for j in self.p:
                if j == p:
                    f += 1
                else:
                    h.append(j)
            self.p = h + ([f*p] if f > 1 else ([] if f == 0 else [p]))

    def __optim_consts(self):
        v = 0
        h = []
        for p in self.p:
            if type(p) == const:
                v += p.v
            else:
                h.append(p)
        self.p = h
        if v != 0:
            self.p.append(const(v))

    def optim(self):
        self.p = self.get_optim_p()
        self.__optim_local_func__()
        k = []
        for p in self.p:
            if not (p is None or (type(p) == const and p.v == 0)):
                if type(p) == add:
                    k += p.get_optim_p()
                else:
                    j = p.optim()
                    if j != None:
                        k.append(j)
        self.p = k
        self.__optim_consts()
        while None in self.p:
            self.p.remove(None)
        l = len(self.p)
        if l > 1:
            return self
        else:
            if l == 0:
                return const(0)
            if l == 1:
                return self.p[0]


class mul(__node):
    def __init__(self, *parents) -> None:
        super().__init__("mul_node", *parents)

    def diff(self, param_name) -> 'add':
        return add(*[mul(*[k.diff(param_name) if i == j else k for j, k in enumerate(self.p)]) for i, n in enumerate(self.p)])

    def get_value(self):
        o = 1
        for i in self.p:
            o *= i.get_value()
        return o

    def update_value(self):
        self.v = 1
        for i in self.p:
            self.v *= i.v

    def __str__(self) -> str:
        return f"{str_sum(*self.p, sep='*')}"

    def __mul__(self, b: '__node'):
        return mul(*self.p, to_node(b))

    def __optim_consts(self):
        v = 1
        h = []
        for p in self.p:
            if type(p) == const:
                v *= p.v
            else:
                h.append(p)
        self.p = h
        if v != 1:
            self.p.append(const(v))

    def __optim_local_func__(self):
        for p in self.p:
            f = 0
            h = []
            for j in self.p:
                if j == p:
                    f += 1
                else:
                    h.append(j)
            self.p = h + ([p**f] if f > 1 else ([] if f == 0 else [p]))

    def optim(self):
        self.p = self.get_optim_p()
        self.__optim_local_func__()
        k = []
        NEGAT = 0
        for p in self.p:
            if (type(p) == const and p.v == 0):
                return const(0)

            if not (p == None or (type(p) == const and p.v == 1)):
                if type(p) == mul:
                    k += p.get_optim_p()
                else:
                    j = p.optim()
                    if j != None:
                        if type(j) == negative:
                            k.append(to_node(-1))
                            k.append(j.p[0])
                        else:
                            k.append(j)
        self.p = k
        self.__optim_consts()
        self.__optim_local_func__()
        l = len(self.p)
        if l > 1:
            if NEGAT % 2:
                return negative(self)
            else:
                return self
        else:
            if l == 0:
                return None
            if l == 1:
                if NEGAT % 2:
                    return negative(self.p[0])
                else:
                    return self.p[0]


class negative(__node):
    def __init__(self, parent) -> None:
        super().__init__('negative_node', parent)

    def get_value(self):
        return -self.p[0].get_value()

    def update_value(self):
        self.v = -self.p[0].v

    def diff(self, param_name) -> '__node':
        return negative(self.p[0].diff(param_name))

    def __str__(self) -> str:
        return f"(-{str(self.p[0])})"
    
    def replace_is_parent_nodes(self, old, new):
        return self.p[0].replace_is_parent_nodes(old, new)

    def replace_eq_parent_nodes(self, old, new):
        return self.p[0].replace_eq_parent_nodes(old, new)
    
    def replace_eq_parent_node(self, new):
        return self.p[0].replace_eq_parent_node(new)

    def optim(self):
        if len(self.p) == 0:
            return None
        if type(self.p[0]) == const:
            return const(-self.p[0].v)
        return super().optim()

class cos(__node):
    def __init__(self, parent) -> None:
        super().__init__("cos_node", parent)

    def diff(self, param_name) -> '__node':
        return mul(negative(sin(self.p[0])), self.p[0].diff(param_name))

    def get_value(self):
        return math.cos(self.p[0].get_value())

    def update_value(self):
        self.v = math.cos(self.p[0].v)

    def __str__(self) -> str:
        return f"cos({str(self.p[0])})"

class sin(__node):
    def __init__(self, parent) -> None:
        super().__init__("sin_node", parent)

    def diff(self, param_name) -> '__node':
        return mul(cos(self.p[0]), self.p[0].diff(param_name))

    def get_value(self):
        return math.sin(self.p[0].get_value())

    def update_value(self):
        self.v = math.sin(self.p[0].v)

    def __str__(self) -> str:
        return f"sin({str(self.p[0])})"

class exp(__node):
    def __init__(self, parent) -> None:
        super().__init__("exp_node", parent)

    def diff(self, param_name) -> '__node':
        return mul(exp(self.p[0]), self.p[0].diff(param_name))

    def get_value(self):
        return math.exp(self.p[0].get_value())

    def update_value(self):
        self.v = math.exp(self.p[0].v)

    def __str__(self) -> str:
        return f"exp({str(self.p[0])})"

class reverse(__node):
    def __init__(self, parent) -> None:
        super().__init__("reverse_node", parent)

    def diff(self, param_name) -> '__node':
        return mul(negative(reverse(mul(*self.p*2))), self.p[0].diff(param_name))

    def optim(self):
        if type(self.p[0]) == const:
            return const(1/self.p[0].v)

        if type(self.p[0]) == pow_node:
            return pow_node(self.p[0].p[0], -self.p[0].n)
        return self

    def get_value(self):
        return 1/self.p[0].get_value()

    def update_value(self):
        self.v = 1/self.p[0].v

    def __str__(self) -> str:
        return f"(1/{str(self.p[0])})"


class sigmoid(__node):
    def __init__(self, parent) -> None:
        super().__init__("sigmoid_node", parent)

    def diff(self, param_name) -> '__node':
        q = sigmoid(self.p[0])
        return mul(q, add(to_node(1), negative(q)), self.p[0].diff(param_name))

    def get_value(self):
        return 1/(1+math.exp(-self.p[0].get_value()))

    def update_value(self):
        self.v = 1/(1+math.exp(-self.p[0].v))

    def __str__(self) -> str:
        return f"q({str(self.p[0])})"

    def __eq__(self, b: '__node') -> bool:
        r = type(self) == type(
            b) and self.name == b.name and self.p[0] == b.p[0]
        return r


class pow_node(__node):
    def __init__(self, base, n) -> None:
        super().__init__(f"pow_node{n}type", base, value=0)
        self.n = n

    def get_value(self):
        return pow(self.p[0].get_value(), self.n)

    def __eq__(self, b: '__node') -> bool:
        return (self is b) or type(self) == type(b) and b.n == self.n and self.p[0] == b.p[0]

    def update_value(self):
        self.v = pow(self.p[0].v, self.n)

    def diff(self, param_name) -> '__node':
        return self.n * pow_node(self.p[0], self.n - 1) * self.p[0].diff(param_name)

    def optim(self):
        if self.n == 1:
            return self.p[0]
        if self.p[0] == const:
            return const(pow(self.p[0].get_value(), self.n))
        return super().optim()

    def __str__(self) -> str:
        return f"({str(self.p[0])}^{self.n})"

    def __mul__(self, b: '__node') -> '__node':
        if type(b) == pow_node and b.p[0] == self.p[0]:
            return pow_node(self.p[0], self.n + b.n)
        return super().__mul__(b)


def hsum(*lists):
    if len(lists) <= 1:
        return lists[0]
    o = lists[0]
    for a in lists[1:]:
        for nl in range(len(o)):
            if nl < len(a):
                o[nl] += a[nl]
            else:
                break  # Prevent out-of-range access
    return o


class program:
    def __init__(self, code: dict[str, "__node"]) -> None:
        self.c = code
        for key, c in self.c.items():
            c.optim()
        self.comp_layers = hsum(*[c.get_deep() for c in self.c.values()])
        self.input_signature = {
            node.name: node for layer in self.comp_layers for node in layer if isinstance(
                node, variable) and type(node) is not const}
        self.__consts = {
            node.name: node for layer in self.comp_layers for node in layer if type(node) is const}
        self.remove_equal_nodes()
        self.comp_layers = hsum(*[c.get_deep() for c in self.c.values()])


    def __call__(self, **kwargs):
        for name, val in kwargs.items():
            if name in self.input_signature:
                self.input_signature[name].v = val
        return self.run()

    def run(self) -> dict[str, any]:
        for j in self.comp_layers:
            for l in j:
                l.update_value() # проверить реализацию
        return {key: c.v for key, c in self.c.items()}

    def remove_equal_nodes(self):
        for l, n in enumerate(self.comp_layers):
            k = []
            for j in n:
                if j not in k:
                    k.append(j)
            self.comp_layers[l] = k
        for l, n in enumerate(self.comp_layers[:-1]):
            for j in n:
                for c in self.c.values():
                    c.replace_eq_parent_node(j)

    def __str__(self) -> str:
        o = ""
        for j in self.comp_layers:
            o += str_sum(*j, sep=",")
            o += "\n"
        return o
