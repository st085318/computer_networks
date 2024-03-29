# Транспортный уровень. Домашка

## Задачи
1.
    >$$T_W(RTT) = \alpha RTT, \alpha > 0$$
    >$$V_W(RTT) = \frac{3}{4}\frac{W}{RTT}, \text{где $V_W$ - средняя пропускная способность}$$
    >$$T_W(V) = \alpha \frac{3}{4}\frac{W}{V}$$

3.
    >Нужно превратить $\frac{W}{2}$ в $W$ с помощью умножения на константу $1 + \alpha$. Для этого нам понадобится $steps=\log_{1 + \alpha} 2$ шагов, что является константой.
    >Тогда задержка между двумя последовательными потерям равна $steps \cdot RTT$ - константа при константности $RTT$.
    >$$L = \frac{1}{steps \cdot RTT} = const$$

4.
    >$4 \times RTT_FE$ возникает из подключения к внешнему серверу (аналогично пояснию из условия) - одно окно для установления соединения и три для доставки ответа. Но внешнему серверу еще самому нужно узнать ответ у дата центра - это займет еще только $RTT_BE$ времени, так как соединение всегда открыто.
    >Тогда общее время равно $4 \times RTT_FE + RTT_BE$