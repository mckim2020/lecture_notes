# DSP_Fall_2020_KAIST

This file is for KAIST students who are taking Digital Signal Processing (EE432), especially regarding filter design using MATLAB.

-------------------------
# Filter Design Basics

## 0. 기본기 - 들어가기 앞서
### 0.1 MATLAB functions
Matlab 에서는 임의의 n개의 변수를 받아 임의의 k개의 변수를 창출해내는 행위가 가능하다. 
사용법은 간단하고 대부분 다음과 같다. 
<pre>
<code>
[n, Wc] = cheb1ord(Wp, Ws, atp, ats, 's'); %Find order(n) and cutoff freq(Wc)

</code>
</pre>

### Filter Design Functions Descriptions

#### Optimizing / Prototypes
> [Cheby1ord](https://www.mathworks.com/help/signal/ref/cheb1ord.html)

> [cheby1](https://www.mathworks.com/help/signal/ref/cheby1.html)

> [cheb2ord](https://www.mathworks.com/help/signal/ref/cheb2ord.html?searchHighlight=cheby2ord&s_tid=srchtitle)

> [cheby2](https://www.mathworks.com/help/signal/ref/cheby2.html)

> [buttord](https://www.mathworks.com/help/signal/ref/buttord.html?searchHighlight=buttord&s_tid=srchtitle)

> [butter](https://www.mathworks.com/help/signal/ref/butter.html?searchHighlight=butter&s_tid=srchtitle)

> [ellipord](https://www.mathworks.com/help/signal/ref/ellipord.html)

> [elllip](https://www.mathworks.com/help/signal/ref/ellip.html)

#### Transformation 
> [bilinear](https://www.mathworks.com/help/signal/ref/bilinear.html?searchHighlight=bilinear&s_tid=srchtitle)

> [impinvar](https://www.mathworks.com/help/signal/ref/impinvar.html?searchHighlight=impinvar&s_tid=srchtitle)

> [tf2zp](https://www.mathworks.com/help/signal/ref/tf2zp.html)

> [lp2lp](https://www.mathworks.com/help/signal/ref/lp2lp.html?searchHighlight=lp2lp&s_tid=srchtitle)

#### System Function Representation 

> [tf](https://www.mathworks.com/help/signal/ref/tf.html?searchHighlight=tf&s_tid=srchtitle)

> [Anothertf](https://www.mathworks.com/help/dsp/ref/dsp.notchpeakfilter.tfnotchpeakfilter.html)

> [zpk](https://www.mathworks.com/help/signal/ref/zpk.html)

#### Windowing 

> [rectwin](https://www.mathworks.com/help/signal/ref/rectwin.html)

>[impz](https://www.mathworks.com/help/signal/ref/impz.html#mw_24b4e23a-81f9-4d8f-a24b-ac6a756a35c7)

>[fir1](https://www.mathworks.com/help/signal/ref/fir1.html)

>[designfilt](https://www.mathworks.com/help/signal/ref/designfilt.html)



Note: 둘 사이 변환을 위한 함수는 다음과 같이 사용한다. 
<pre>
<code>
tf2zp(b, a); % Transfer function to Zero Pole K(constant)

zp2tf(bz, az, k); % Zero Pole K(constant) to Transfer function 

</code>
</pre>

### 0.2 Tools
<pre>
<code>
zplane(bz, az); % Z-plane 그릴 때

freqs(b, a) % System function이 s 에 대한 함수일 경우 == Transfer function

freqz(bz, az) % System function이 z에 대한 함수일 경우

fvtool(bz, az); % System 의 frequency response 분석 도구

</code>
</pre>

# 0.3 ???
---------------------------------------------
## 1. Impulse Invariance Method
### 1.1 Normalization of bands
먼저, Passband과 Stopband 두 경계선을 Td, 즉 sampling interval 로 나누어 주는 Band Normalization을 진행한다. 

<pre>
<code>
Wp = wp / Td; % Pass Band

Ws = ws / Td; % Stop Band 

</pre>
</code>

### 1.2 Find analog filter prototype
다음으로 Matlab 에 내재되어 있는 함수를 이용하여, 필터의 조건을 충족시키는 최적의 N(order) 값과 Wc(Cutoff Frequency) 값을 구해낸다. 

<pre>
<code>
[n, Wc] = cheb1ord(Wp, Ws, atp, ats, 's');

</pre>
</code>

이후, system function 꼴로 나타내어준다. (Frequency response)

<pre>
<code>
[b, a] = cheby1(n, atp, Wc, 's');

</pre>
</code>

### 1.3 Cutting the edge
필터 설계시, 1.2 단계에서 구한 cutoff frequency, Wc 에 맞추어, system function 을 알맞게 추려낸다. 

<pre>
<code>
[bt, at] = lp2lp(b, a, Wc);

</pre>
</code>

달리 말해, 아날로그 필터에 맞추어 Wp(pass band)와 Ws(stop band) 등을 조정해주는 기능이다. 


### 1.4 Transformation 
Matlab에 내재된 impinvar(systemVar1, systemVar2, fs) 함수를 이용하여, z transform 의 꼴로 변환된 "new system function"을 얻도록 하자.

<pre>
<code>
[bz, az] = impinvar(bt, at, 1/Td);

</pre>
</code>

-------------------------------------------------------
## 2. Bilinear Method
### 2.1 Transformation of variables
Laplace transform의 s plane 으로부터 Z transform 의 z plane 으로 옮겨오는 과정이다. 
S-plane 의 y축, 즉 허수 부분은 Z-plane 의 unit circle 에 해당함을 기억하자. 
변환식은 다음과 같다. 
<pre>
<code>
Wp = 2/Td * tan(wp/2);

Ws = 2/Td * tan(ws/2);

</pre>
</code>

### 2.2 Find analog filter prototype
다음으로 Matlab 에 내재되어 있는 함수를 이용하여, 필터의 조건을 충족시키는 최적의 N(order) 값과 Wc(Cutoff Frequency) 값을 구해낸다. 

<pre>
<code>
[n, Wc] = cheb1ord(Wp, Ws, atp, ats, 's');

</pre>
</code>

이후, system function 꼴로 나타내어준다. (Frequency response)

<pre>
<code>
[b, a] = cheby1(n, atp, Wc, 's');

</pre>
</code>

### 2.3 Cutting the edge
필터 설계시, 1.2 단계에서 구한 cutoff frequency, Wc 에 맞추어, system function 을 알맞게 추려낸다. 

<pre>
<code>
[bt, at] = lp2lp(b, a, Wc);

</pre>
</code>

달리 말해, 아날로그 필터에 맞추어 Wp(pass band)와 Ws(stop band) 등을 조정해주는 기능이다. 


### 2.4 Transformation 
Matlab에 내재된 bilinear(systemVar1, systemVar2, fs) 함수를 이용하여, z transform 의 꼴로 변환된 "new system function"을 얻도록 하자.

<pre>
<code>
[bz, az] = impinvar(bt, at, 1/Td);

</pre>
</code>
