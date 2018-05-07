---
title: Scionics - Data-Driven Consulting
author: Peter Steinbach
origin: Scionics Computer Innovation GmbH
email: steinbach@scionics.de
date: May 17, 2018, Airbus Defence
---


# Real-life performance optimisation is never

## as simple as this

.container-fluid[

.row align-items-center[

.col[

![](img/allinea_performance_roadmap.jpg){ class="figure-img img-fluid" width="70%" }

.]

.]

.]


## more like this


.container-fluid[

.row align-items-center[

.col[

![](img/dark_Odysseus_Journey_zoom.png){ class="figure-img img-fluid" width="100%" }

.]

.]

.]


## Agenda 

0. Motivation
1. Who-am-I
2. Performance outside-in
3. Performance inside-out
4. Benchmarks and how to create them


# Who-am-I and Motivation

## Who am I?

.container-fluid[

.row align-items-center[

.col[

![](img/events_header_m_quarter.jpg){ class="figure-img img-fluid" width="50%" }

.]

.col[

**[Scionics Computer Innovation GmbH](www.scionics.de)**

- software and consulting company
- founded in 2001 in Dresden, Germany
- expertise in data analysis, bioinformatics, image analysis, HPC, ...

.]

.]

.]


:notes[

- 2h by car south of Berlin  
- NEXT: biggest client = CBG

:]



## Our Client


.container-fluid[

.row align-items-center[

.col[

![MPI for Molecular Cell Biology and Genetics](img/800px-MPI-CBG_building_outside_4pl.jpg){ class="figure-img img-fluid" width="100%" }

[mpi-cbg.de](www.mpi-cbg.de)

.]

.col[

- 500+ staff
- my role: *Scientific Software Engineer*
- support users on our HPC infrastructure
- software projects related to performance (think multi-threaded, GPUs, ..)

.]

.]

.]


:notes[

- biggest client
- NEXT: How does my day look like sometimes ...

:]



## Disclaimer


.container-fluid[

.row justify-content-center[

  .col[

![](img/opensource-550x475.png){ class="figure-img img-fluid" width="40%" }  

**[github.com/psteinb/parallel2018](https://github.com/psteinb/parallel2018)**


  .]

.]

.]


:notes[

report bugs and questions there!

:]


## Before I begin


.container-fluid[

.row align-items-center[

.col-8[


![[Mars Climate Orbiter (1998)](https://en.wikipedia.org/wiki/Mars_Climate_Orbiter#Encounter_with_Mars)](img/Mars_Climate_Orbiter_2.jpg){ class="figure-img img-fluid" width="70%" }  


  .]

.col-4[

> All of my slides assume, that the code provides correct results!

. . .

> Nobody wants fast code, that is wrong!

.]

.]

.]



# Performance Outside-In


## One day as a Performance Engineer

![Alan O'Rourke, [Too Busy To Improve - Performance Management - Square Wheels](https://www.flickr.com/photos/toddle_email_newsletters/15412982829/in/photostream/), CC](img/flickr_ORourke_2_busy_to_improve_framed.png){ class="figure-img img-fluid" width="70%" }

:notes[

- scientists typically develop algorithms (to publish)
- performance is important for usablity

:]

## Once in a while { data-background-image="img/frustration-cry-1682140_1920.jpg" }

.container-fluid[

.row align-items-center[

.col-8[

```
From: doe@theinstitute.de
Subject: Cluster is slow
Date: Fri, 20 Oct 2017 12:03:21 +0200
To: hpcsupport@theinstitute.de

Hi,

what is going on with the cluster? My application is running
slow since yesterday.
Could you have a look at it please?

Thanks,
John
```

.]

.]

.]


:notes[

- speed is a subjective measure
- performance is a matter of perspective
- note: description for reproducibility missing
- https://youtu.be/FnGCDLhaxKU?t=6152

:]



## Challenge: Finding the performance regression without looking at the code {  data-background-image="img/traffic_jam_800px.png" data-background-position="right" style="background: rgba(105,105,105, 0.8); border-radius: 20px;" }

:notes[

- find the street with the traffic jam
- experience guided

:]



## High Level Overview


.container-fluid[

.row align-items-center[

.col[

![[htop](http://hisham.hm/htop/), [free](https://linux.die.net/man/1/free) et al](img/htop_in_action.png){ class="figure-img img-fluid" width="90%" }

.]

.col[

![](img/task_manager_small.png){ class="figure-img img-fluid" width="80%" }

.]

.]

.]


## Reference Numbers

```
$ dd if=/dev/zero of=/tmp/just_zeros bs=1G count=2
2+0 records in
2+0 records out
2147483648 bytes (2.1 GB) copied, 2.94478 s, 729 MB/s

$ dd if=/dev/zero of=/dev/shm/2gb.zeros bs=1G count=2
2+0 records in
2+0 records out
2147483648 bytes (2.1 GB) copied, 1.14782 s, 1.9 GB/s
```

&nbsp;

**What can your hardware typically do?**  

dd, [ior](http://www.nersc.gov/users/computational-systems/cori/nersc-8-procurement/trinity-nersc-8-rfp/nersc-8-trinity-benchmarks/ior/), memhog,  [stream](https://www.cs.virginia.edu/stream/), ...


:notes[

- to search for the bottleneck, know your performance without it
- guesstimate the bottleneck, cross check expected performance with a benchmark

]


## Profile with [perf](https://perf.wiki.kernel.org/index.php/Main_Page)

.container-fluid[

.row align-items-center[

  .col-9[


```
$ perf record -g ./my-slow-binary
[ perf record: Woken up 1 times to write data ]
[ perf record: Captured and wrote 0.023 MB perf.data (75 samples) ]
$ perf report --stdio
no symbols found in /usr/bin/dd, maybe install a debug package?
# ...
# Total Lost Samples: 0
#
# Samples: 75  of event 'cycles:u'
# Event count (approx.): 1839654
#
# Children      Self  Command  Shared Object      Symbol           
# ........  ........  .......  .................  ................
#
    20.18%    20.18%  dd       [kernel.kallsyms]  [k] page_fault
            |          
             --19.77%--0
                       _int_realloc
                       page_fault
```

  .]

  .col-3[

  - lightweight sample based profiling 
  - per task, per CPU and per-workload counters
  - sample CPU performance counters, tracepoints or system probes
  - on windows: [xperf](https://docs.microsoft.com/en-us/windows-hardware/test/wpt/wpt-getting-started-portal)/[UIforETW](https://github.com/google/UIforETW)
  
  .]

.]

.]

## perf: what is a callstack? 

.container-fluid[

.row align-items-center[

  .col[

  <object type="image/svg+xml" data="figure/stacktrace_illustration/stacktrace_dark.svg" width="40%">
  Your browser does not support SVG
  </object>

  .]
  
.]

.]
  

## perf: sampling based profiling 

.container-fluid[

.row align-items-center[

.col-8[

  <object type="image/svg+xml" data="figure/stacktrace_illustration/stacktrace_dark_with_traces.svg" width="60%">
  Your browser does not support SVG
  </object>

  .]

.col-4[

- for every sampling event:
    + record call stack
    + query hardware counters, e.g. cpu-cycles
- sampling must not be accurate

.]


.]

.]


:notes[

- hardware counters = low overhead
- missing accuracy != problem on nondeterministic system

:]



## [perf](https://perf.wiki.kernel.org/index.php/Main_Page) Reloaded with [FlameGraphs](https://github.com/brendangregg/FlameGraph)


.container-fluid[

.row align-items-center[

  .col-8[


```
$ perf record -g ./my-slow-binary
[ perf record: Woken up 1 times to write data ]
[ perf record: Captured and wrote 0.023 MB perf.data (75 samples) ]
$ perf script > out.perf
$ ./stackcollapse-perf.pl out.perf > out.folded
$ ./flamegraph.pl out.folded > perf_samples.svg
```

  .]

  .col-4[

  - visualisation technique conceived by [Brendan Gregg](https://github.com/brendangregg) (Netflix)
  - seamless integration into perf, dtrace, systemtap, XCode Instruments, Lightweight Java Profiler, Microsoft Visual Studio profiles, ...
  - based on collected counter samples and the stacktrace they were collected in
  
  .]

.]

.]


## Ethereum Mining [as FlameGraph](figure/flamegraph/ethminer-cuda-simulate.svg)

.container-fluid[

.row align-items-center[

  .col[
  
  <object type="image/svg+xml" data="figure/flamegraph/ethminer-cuda-simulate.svg" width="90%">
  Your browser does not support SVG
  </object>

  .]

.]

.]


.container-fluid[

.row align-items-start[

  .col[

  - (x axis) current stack level in alphabetical order  
  
  .]

  .col[
  
  - (y axis) number of samples in that stacktrace level

  .]

.]

.]

:notes[

- alphetical ordering inside each stacktrace level

:]


## HPC user's slow application

.container-fluid[

.row align-items-center[

  .col[
  
  <object type="image/svg+xml" data="figure/flamegraph/hpc_user.svg" width="90%">
  Your browser does not support SVG
  </object>

  .]

.]

.]


:notes[

- this graph = cpu_cycles; alternative = i/o flamegraph
- **so far**: didn't touch the source code or build it

:]


## Bottom Line { data-background-image="img/balloon.jpeg" style="background: rgba(105,105,105, 0.8); border-radius: 20px;"}

Taking a balloon to get an overview of performance bottlenecks is possible.



# Performance Inside-Out {  data-background-image="img/cable_chaos.jpg" style="background: rgba(105,105,105, 0.8); border-radius: 20px;" }


## High Diversity of Tools! { data-background-image="img/dreamstime-in-c++.jpg" data-background-position="right" style="background: rgba(105,105,105, 0.8); border-radius: 20px;"}

:notes[

- tricky to recommend one only
- tricky to find cross platform one
- typical: develop/profile on one platform, choose deploy on all
- now: brief tour

:]


## [valgrind](valgrind.org) + kcachegrind

.container-fluid[

.row align-items-center[

  .col[
  
  ![](img/kcachegrind-screenshot.png){ class="figure-img img-fluid" width="80%" }  
  
  .]

.]

.]


Profile from [Peter Gottschling's example on vector unrolling](https://github.com/petergottschling/discovering_modern_cpp/blob/master/c%2B%2B11/vector_unroll_example.cpp).


:notes[

- pseudo-vm is the only way to obtain a line profile in C++
- x86 translated to RISC-like syntax `UCode`
- heavy performace hit

:]


## Simple Graphical output, [perftools](https://github.com/gperftools/gperftools)

.container-fluid[

.row align-items-center[

  .col[
  
  ![](figure/profiling/perftools/pprof21143.0.png){ class="figure-img img-fluid" width="90%" }  
  
  .]

.]

.]

Profile from [Peter Gottschling's example on vector unrolling](https://github.com/petergottschling/discovering_modern_cpp/blob/master/c%2B%2B11/vector_unroll_example.cpp).

:notes[

- results can be converted to kcachegrind compatible format
- small performace hit

:]

## Using flamegraphs, [hotspot](https://www.kdab.com/hotspot-gui-linux-perf-profiler/)

.container-fluid[

.row align-items-center[

  .col[
  
  ![](img/hotspot.png){ class="figure-img img-fluid" width="80%" }  
  
  .]

.]

.]


:notes[

- thanks to Millian Wolff (KDAB)
- well done OSS tool with bright future

:]

## [xray](https://llvm.org/docs/XRay.html)

  
```
$ CXX=clang++ make

$ XRAY_OPTIONS="patch_premain=true xray_mode=xray-basic verbosity=1" 
$ ./vector_unroll_example
==31936==XRay: Log file in 'xray-log.vector_unroll_example.ju4PNk'
Compute time native loop is 0.159 micros.
u[0] is 15
#...

$ llvm-xray account xray-log.vector_unroll_example.ju4PNk -instr_map=./vector_unroll_example
nctions with latencies: 5
 funcid      count [      min,       med,       90p,  ...]       sum  function    
      1          1 [ 7.338530,  7.338530,  7.338530,  ...]  7.338530  <invalid>:0:0: main
      2       1275 [ 0.000005,  0.000011,  0.000012,  ...]  0.013064  <invalid>:0:0: void my_axpy<2u, vector<float>, vector<float>, vector<float> >(vector<float>&, vector<float> const&, vector<float> const&)
```

:notes[

- introduced in llvm4
- flamegraph output available since llvm6
- latency focussed 

:]

## Proprietary tools

.container-fluid[

.row align-items-center[

  .col[
  
  ![](img/intel_advisor_2017.png){ class="figure-img img-fluid" width="80%" }  
  
  .]

.]

.]


:notes[

- excellent tool from the docs
- would love to afford it
- NEXT: hotspot found

:]


## Found a hot spot! { data-background-image="img/1024px_light-bulb-light-old.jpg" data-background-position="right" }


:notes[

- search finished, critical function/class identified
- NOW: find out why it is slow?

:]


## Danger zone of mental models { data-background-image="img/slip-up-danger-careless-slippery.jpg" data-background-position="right" style="background: rgba(105,105,105, 0.8); border-radius: 20px;" }

:notes[

- mental models are often wrong or outdated
- with a colleaque or rubber duck, come up with falsifyable hypothesis!

:]


## Inspect Assembly?

.container-fluid[

.row align-items-center[

  .col[
  
  ![](img/compiler_explorer.png){ class="figure-img img-fluid" width="100%" }  
  
  .]

.]

.]


:notes[

- inspecting assembly tough!
- play with -O flags to get a feeling
- mental hardware model can still be wrong
- asm can only partially falsify hypothesis

:]


## perf for hardware exploration?

.container-fluid[

.row align-items-center[

.col-9[

```
$ perf list

List of pre-defined events (to be used in -e):

  branch-instructions OR branches                    [Hardware event]
  branch-misses                                      [Hardware event]
  bus-cycles                                         [Hardware event]
  cache-misses                                       [Hardware event]
  cache-references                                   [Hardware event]
  cpu-cycles OR cycles                               [Hardware event]
  instructions                                       [Hardware event]
  ref-cycles                                         [Hardware event]
  stalled-cycles-frontend OR idle-cycles-frontend    [Hardware event]
  #...
  L1-dcache-load-misses                              [Hardware cache event]
  L1-dcache-loads                                    [Hardware cache event]
  L1-dcache-prefetch-misses                          [Hardware cache event]
  L1-dcache-store-misses                             [Hardware cache event]
  L1-dcache-stores                                   [Hardware cache event]
  L1-icache-load-misses                              [Hardware cache event]
  #...
```

.]

.col-3[


- perf event list depends on kernel version
- hardware counters are not portable (specification change by vendors)
- alternative: [ocperf](https://github.com/andikleen/pmu-tools)


.]

.]

.]


:notes[

- I prefer LIKWID

:]


## Test hypothesis with [likwid](https://github.com/RRZE-HPC/likwid)

.container-fluid[

.row align-items-center[

  .col[
  
  ![](img/likwid-repo.png){ class="figure-img img-fluid" width="90%" }
  
  .]

.]

.]

.container-fluid[

.row align-items-start[

.col[

- [github.com/RRZE-HPC/likwid](https://github.com/RRZE-HPC/likwid)
- open source Performance monitoring and benchmarking suite
- Linux only

.]

.col[

- profiling through hardware counters (consistent meta markers for portability)
- exploration through monitoring
- marker API for C, C++, java and python

.]

.]

.]


## use case: Index Lists

.container-fluid[

.row align-items-center[

.col-9[


```
#include <vector>
#include "omp.h"

struct item{
    std::vector<float> position, momentum;
    std::vector<int>   nearest_neighbors;}

int main(int argc, char** argv){
    std::vector<item> world = generate(argc*10e6);
    
    for(int& time_step : timelapse){
        update(world);
        
        #pragma omp parallel for
        for(item& it : world){
            for(int& index : it.nearest_neighbors){
                auto distance = calculate(it, world[index]);
                if(distance > threshold)
                    it.nearest_neighbors.remove(index);
            }}}
    //..
}
```

.]

.col-3[

- **hypotheses**:  

    + large 'unpredictable' jumps in memory access diminishes cache bandwidth
    
    + [false sharing](https://en.wikipedia.org/wiki/False_sharing) forces cache line reloads as read-only and writable items may share the same cache line

. . . 


Let's measure!


.]

.]

.]


:notes[

- code has a lot of problems related to memory layout
- index of nearest neighbor `item` stored in vector
- only show measurement for false sharing for brevity

:]

## use case: Through Likwid

.container-fluid[

.row align-items-start[

.col-6[

Use Case

```
# export OMP_NUM_THREADS=1
# path/to/likwid-perfctr -f -c 0 -g FALSE_SHARE \
numactl -m0 -C0 ./my_app
+----------------------------------|--------------+
|              Metric              |    Core 0    |
+----------------------------------|--------------+
//..
|  Local LLC false sharing [MByte] |       0.0008 |
|   Local LLC false sharing rate   | 5.608215e-10 |
//..
+----------------------------------|--------------+

# export OMP_NUM_THREADS=4
# path/to/likwid-perfctr -f -c 0-4 -g FALSE_SHARE \
numactl -m0 -C0-3 ./my_app
+---------------------------------------|--------------|
|                 Metric                |      Sum     |
+---------------------------------------|--------------|
#..
|  Local LLC false sharing [MByte] STAT |    2973.7637 |
|   Local LLC false sharing rate STAT   |       0.0081 |
#..
+---------------------------------------|--------------|
```

.]



.col-6[

Stream Benchmark as Reference

```
# export OMP_NUM_THREADS=1
# path/to/likwid-perfctr -f -c 0 -g FALSE_SHARE \
numactl -m0 -C0 ./stream
+----------------------------------|--------------+
|              Metric              |    Core 0    |
+----------------------------------|--------------+
#..
|  Local LLC false sharing [MByte] |       0.0006 |
|   Local LLC false sharing rate   | 6.057282e-10 |
#..
+----------------------------------|--------------+

# export OMP_NUM_THREADS=4
# path/to/likwid-perfctr -f -c 0-4 -g FALSE_SHARE \
numactl -m0 -C0-3 ./stream
+---------------------------------------|--------------|
|                 Metric                |      Sum     |
+---------------------------------------|--------------|
#..
|  Local LLC false sharing [MByte] STAT |       0.1067 |
|   Local LLC false sharing rate STAT   | 4.080027e-07 |
#..
+---------------------------------------|--------------|
```

.]

.]

.]





## Bottom Line

.container-fluid[

.row align-items-center[

.col[

- excellent tools available to find hot spots
- once "found", talk to someone  
(rubber duck or colleaque(s))
- create falsifiable hypotheses
- MEASURE!


.]



.col[

![["Rubber Duckie, You're the One", by Daniel Rothamel, CC-BY 2.0](https://www.flickr.com/photos/realestatezebra/2608418319)](img/rubber_duck_with_glasses.jpg){ class="figure-img img-fluid" width="100%" }

.]

.]

.]



:notes[

- NEXT: let's find alternative code paths (algorithms/technology)

:]


# Benchmarks and how to create them { data-background-image="img/dark_Odysseus_Journey_500less_1200px.png" style="margin-top: -200px; background: rgba(1,21,26, 0.8); border-radius: 20px;" }

## faster code?

[Chandler Carruth, Understanding Compiler Optimization, MeetingCPP 2015](https://youtu.be/FnGCDLhaxKU?t=6143)

> Klaus Iglberger: Guys that do know a lot about performance, do a lot of manual unrolling (manual vectorization). Apparently they don't trust the compiler too much. What is your take on this?

. . .

> Chandler: How do you define "people who know a lot about performance"? Serious question. So I work with Google's optimisation team who is responsible for making our C++ code run fast. And I have never seen them manually unroll a loop. 


## chrono is your friend

```
#include <chrono>
#include <iostream>
#include "production_code.hpp"
#include "new_ideas.hpp"

int main(int argc, char** argv){

    auto start = std::chrono::high_resolution_clock::now();
    auto result = production_code::algorithm();
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> t_p = (end - start);
    
    start = std::chrono::high_resolution_clock::now();
    auto new_result = new_ideas::algorithm();
    end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> t_i = (end - start);

    std::cout << "we achieved a speed-up of " << t_p.count()/t_i.count() 
              << std::endl;
              
    return 0;
}
```

## ... check for correctness

```
#include <chrono>
#include <iostream>
#include "production_code.hpp"
#include "new_ideas.hpp"

int main(int argc, char** argv){

    auto start = std::chrono::high_resolution_clock::now();
    auto result = production_code::algorithm();
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> t_p = (end - start);
    
    start = std::chrono::high_resolution_clock::now();
    auto new_result = new_ideas::algorithm();
    end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> t_i = (end - start);

    if(result == new_result)
        std::cout << "we achieved a speed-up of " << t_p.count()/t_i.count() 
                  << std::endl;
    else
        std::cout << "Never mind!" << std::endl;
}
```

## noisy lab under your fingers


```
#include ...

int main(int argc, char** argv){

    auto result = 0;
    auto new_result = 0;
    
    auto start = std::chrono::high_resolution_clock::now();

    for(int i = 0;i<n_repetitions;++i)
        result = production_code::algorithm();
   
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> t_p = (end - start);
    
    start = std::chrono::high_resolution_clock::now();
    
    for(int i = 0;i<n_repetitions;++i)
        new_result = new_ideas::algorithm();
        
    end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> t_i = (end - start);

    if(result == new_result)
        std::cout << "we achieved a speed-up of " << t_p.count()/t_i.count() 
                  << std::endl;
    else
        std::cout << "Never mind!" << std::endl;
}
```

## Please take notes

```
#include ...

using duration_t = std::chrono::duration<double>;

int main(int argc, char** argv){
    //..
    auto start = std::chrono::high_resolution_clock::now();
    auto end = start;
    std::vector<duration_t> my_timings(n_repetitions);

    for(int i = 0;i<n_repetitions;++i){
        start = std::chrono::high_resolution_clock::now();
        result = production_code::algorithm();
        my_timings[i] = std::chrono::high_resolution_clock::now() - start;
    }
   
    //same with new_result = new_ideas::algorithm()

    if(result == new_result){
        std::ofstream ofile("results.csv");ofile.open();
        for(int i = 0;i<n_repetitions;++i){
            ofile << i << ",production," << prod_timings[i].count() << ",seconds" << std::endl;
        }
        //same with new_idea
        ofile.close()
    }
    else
        std::cout << "Never mind!" << std::endl;
}
```

## Why?

> ... It's a simple Python interface around a blazing fast C++ library ...

[from github.com/vincentlaucsb/csvmorph](https://github.com/vincentlaucsb/csvmorph)

&nbsp;

> ... However C++ code used to be significantly faster for a long time, and also today still is in many cases.

[from SO "How much faster is C++ than C#?"](https://stackoverflow.com/a/138406)

**[see more for youself!](http://lmgtfy.com/?q=C%2B%2B+faster)**

:notes[

- people expect C++ to be faster!!

:]

## Life as a reviewer


.container-fluid[

.row align-items-center[

.col[

![](img/hoefler_scientific_benchmarking_table1.png){ class="figure-img img-fluid" width="100%" }

T. Hoefler et al, ["Scientific Benchmarking of Parallel Computing Systems - Twelve ways to tell the masses when reporting performance results"](https://dl.acm.org/citation.cfm?id=2807644), <br>SC '15 Proceedings, 2015


.]

.]

.]



:notes[

- reviewer for conference proceedings related to GPU programming
- very often: results are not reproducible and not based on ensemble's mean+variance

:]


## Let's take a toy example

.container-fluid[

.row align-items-center[

.col[

![[quick-bench.com](http://quick-bench.com/suql1AKnQ9a5l7ijd6ehwz_iVFk)](img/quick_bench_example.png){ class="figure-img img-fluid" width="100%" }

.]

.]

.]

:notes[

- great tool!!
- use results with a grain of salt

:]

## ... what if

.container-fluid[

.row align-items-center[

.col[

![**Ensemble variances tell a story!**](figure/quick_bench_mock.png){ class="figure-img img-fluid" width="100%" }

.]

.]

.]


:notes[

- again: great tool!!

:]


## Standardized, easy-to-parse output!

.container-fluid[

.row align-items-center[

.col[

![](img/hoefler_scientific_benchmarking_fig1.png){ class="figure-img img-fluid" width="70%" }

T. Hoefler et al, ["Scientific Benchmarking of Parallel Computing Systems - Twelve ways to tell the masses when reporting performance results"](https://dl.acm.org/citation.cfm?id=2807644), <br>SC '15 Proceedings, 2015


.]

.col-4[

> Can't this be automated?

.]

.]

.]




:notes[

- statistics offer much more feature rich interpretation
- allows reproducibility of results
- allows choice of tools for interpretation (Rmarkdown, jupyter notebooks, ...)
- fight the in-silico crisis

:]


## google/benchmark

.container-fluid[

.row align-items-center[

.col[

![[github.com/google/benchmark](https://github.com/google/benchmark)](img/libbenchmark_repo.png){ class="figure-img img-fluid" width="85%" }

.]

.]

.]

&nbsp;

.container-fluid[

.row align-items-center[

.col[

- written in C++11/C++03
- support of multi-threaded applications
- powerful CLI

.]

.col[

- easy setup of (templated) test cases
- flexible argument control
- custom counters/timers

.]

.]

.]

## benchmark: in action

.container-fluid[

.row align-items-center[

.col-8[

![[Matt Godbolt at CppCon2017](https://www.youtube.com/watch?v=smqT9Io_bKo)](img/cppcon_godbolt_reduction.png){ class="figure-img img-fluid" width="100%" }

.]

.col[

__Question:__

> Are range-based for loops faster than integer based ones depending on the data type used?


.]

.]

.]


## benchmark: simple approach

.container-fluid[

.row align-items-start[

.col-6[

```
#include <benchmark/benchmark.h>
#include <vector>

template <typename T>
double sum(const T* _data, std::size_t _len){

    double value = 0;
    for(std::size_t i = 0;i<_len;++i)
        value += _data[i];

    return value;
}

template <typename container_type>
double sum(const container_type& _data){

    typedef typename container_type::value_type value_t;

    double value = 0;
    for(const value_t& el : _data)
        value += el;

    return value;
}
```
.]

.col-6[

```
static void BM_integer_index(benchmark::State& state) {

    const std::size_t len = 1 << 20;
    std::vector<int> values(len,0.f);
    double result = 0;

    for (auto _ : state){
        benchmark::DoNotOptimize(result = sum(values.data(), len));
    }
}
// Register the function as a benchmark
BENCHMARK(BM_integer_index);

static void BM_range_based(benchmark::State& state) {

    const std::size_t len = 1 << 20;
    std::vector<int> values(len,0.f);
    double result = 0;

    for (auto _ : state){
        benchmark::DoNotOptimize(result = sum(values));
    }

}
BENCHMARK(BM_range_based);

BENCHMARK_MAIN();
```

.]

.]

.]

## benchmark: simple approach output

```
Run on (4 X 3600 MHz CPU s)
2017-11-08 10:24:43
***WARNING*** CPU scaling is enabled, the benchmark real time measurements may be noisy and will incur extra overhead.
--------------------------------------------------------
Benchmark                 Time           CPU Iterations
--------------------------------------------------------
BM_integer_index     922920 ns     915531 ns        764
BM_range_based       937344 ns     929681 ns        768
```


## benchmark: advanced

.container-fluid[

.row align-items-center[

.col-7[

```
template <typename T>
static void BM_integer_index(benchmark::State& state) {

    const std::size_t len = state.range(0);
    std::vector<T> values(len,0.f);
    double result = 0;

    for (auto _ : state){
        benchmark::DoNotOptimize(result = sum(values.data(), len));
    }
}

BENCHMARK_TEMPLATE(BM_integer_index,int)
->Arg(64)
->Arg(512)
->Arg(1 << 10)
->Arg(128<<10)
->Arg(1<<20)
->Arg(128<<20);
BENCHMARK_TEMPLATE(BM_integer_index,float)
->Arg(64)
->Arg(512)
->Arg(1 << 10)
->Arg(128<<10)
->Arg(1<<20)
->Arg(128<<20);

BENCHMARK_MAIN();
```
.]

.col[

- multiple arguments are also supported
```
BENCHMARK_TEMPLATE(BM_integer_index,int)
//42 is the initial value of the reduced sum
->Arg({64, 42})
//..
;
```
- templated benchmark cases are supported
- workflow:

. . .

1. build benchmark <br> (different working set sizes, types)
2. compile with varying flags
3. run & inspect
5. render report with [rmarkdown](https://github.com/rstudio/rmarkdown)

.]

.]

.]

:notes[

- too bad: fixtures and templated benchmarks are lacking

:]

## benchmark: advanced output

```
Run on (4 X 3600 MHz CPU s)
2017-11-08 10:25:27
***WARNING*** CPU scaling is enabled, the benchmark real time measurements may be noisy and will incur extra overhead.
-------------------------------------------------------------------------
Benchmark                                  Time           CPU Iterations
-------------------------------------------------------------------------
BM_integer_index<int>/64                  50 ns         50 ns   10000000
BM_integer_index<int>/512                424 ns        423 ns    1634359
BM_integer_index<int>/1024               864 ns        861 ns     772101
BM_integer_index<int>/131072          112125 ns     111777 ns       6344
BM_integer_index<int>/1048576         924382 ns     916717 ns        761
BM_integer_index<int>/134217728    123700290 ns  122614766 ns          6
BM_integer_index<float>/64                52 ns         51 ns   13374011
BM_integer_index<float>/512              427 ns        425 ns    1641151
BM_integer_index<float>/1024             863 ns        860 ns     772552
BM_integer_index<float>/131072        111322 ns     111160 ns       6109
BM_integer_index<float>/1048576       914593 ns     909174 ns        763
BM_integer_index<float>/134217728  122954355 ns  122219776 ns          6
BM_range_based<int>/64                    50 ns         50 ns   13580124
BM_range_based<int>/512                  429 ns        429 ns    1570356
BM_range_based<int>/1024                 866 ns        865 ns     815042
BM_range_based<int>/131072            111289 ns     111139 ns       6316
BM_range_based<int>/1048576           912475 ns     907277 ns        761
BM_range_based<int>/134217728      122509880 ns  121832332 ns          6
BM_range_based<float>/64                  48 ns         48 ns   13944707
BM_range_based<float>/512                426 ns        426 ns    1637659
BM_range_based<float>/1024               863 ns        862 ns     810743
BM_range_based<float>/131072          110915 ns     110775 ns       6343
BM_range_based<float>/1048576         917501 ns     912365 ns        735
BM_range_based<float>/134217728    122908318 ns  122219268 ns          6

```


## benchmark: reproduce this!

.container-fluid[

.row align-items-center[

.col[

![gcc 6.4.1, libbbenchmark 1.3, <br>[code available in this repo](src/libbenchmark/README.md)](src/libbenchmark/comparison_O2.png){ class="figure-img img-fluid" width="100%" }

.]

.col[

- file an [issue](https://github.com/psteinb/meetingcpp2017) if you reproduced this!

```
$ cd /path/to/sliderepo/src/libbenchmark
$ //install libbenchmark & tidyverse R package
$ CXXFLAGS=-O2 make report
$ my-browser report.html
```
.]

.]

.]


## There is more

--------------------------------- ------- --------------------------- ------------------------------------------
 [nickbruun/hayai][haylink]        229    - based on googletest <br>  - no csv output <br>                   
                                          - random order <br>         - online docs? commit activity?<br>
                                          - fixture support           - no donotoptimize <br>
                                                                      - max/min/means reported by default
                                                                                                                                  
 [DigitalInBlue/celero][cellink]   249    - no dependencies <br>      - no csv output <br>
                                          - baseline <br>             - means reported by default
                                          - fixture support           
                                                              
 [nonius.io][nonlink]              49-194 - header-only <br>          - confusing repo structure <br>
                                          - depends on boost <br>     - buggy example(s) <br>
                                          - super statistics summary  - confidence intervals fixed to <br> 
                                                                        normal distribution <br>
                                                                      - no donotoptimize
                                                                                           
 [google/benchmark][benlink]       1985   - no dependencies <br>      - templated versus fixture based setup <br>
                                          - feature rich              - means reported by default  
                           
--------------------------------- ------- --------------------------- -------------------------------------------


[haylink]: https://github.com/nickbruun/hayai
[cellink]: https://github.com/DigitalInBlue/Celero
[nonlink]: https://nonius.io/
[benlink]: https://github.com/google/benchmark

## Where to stop?

- __clearify upfront__
- where is your limit?
    - hardware
    - APIs and libraries
    - dependencies
    - compiler
    - OS

## roofline

.container-fluid[

.row align-items-center[

.col-8[

![[G. Ofenbeck, "Applying the Roofline Model", ISPASS'14 proceedings, 2014](http://www.spiral.net/software/roofline.html)](img/overview-mmm-illustrator.pdf.png){ class="figure-img img-fluid" width="100%" }

.]

.col[

- acknowledge boundaries of algorithm
- differentiate "work" versus "traffic"
- simplistic: bottleneck is either work or traffic
- clear indication where optimisations go

.]

.]

.]

## roofline for real

.container-fluid[

.row align-items-center[

.col-8[

![complex vs. real FFT transforms](img/gearshifft_results_r2c_vs_c2c_a.png){ class="figure-img img-fluid" width="70%" }

.]

.col[

*[gearshifft](https://github.com/mpicbg-scicomp/gearshifft) FFT benchmark*

- co-authored with TU Dresden
- note the variances!
- published at ISC'17

.]

.]

.]

## rooline tooling: [kerncraft](https://github.com/RRZE-HPC/kerncraft)

```
$ cat /tmp/add.c
double a[N], b[N], c[N];

for(int i=0; i<N; ++i)
    a[i] = b[i] + c[i];

```

. . . 


```    
$ kerncraft  -p Roofline -m /tmp/IvyBridgeEP_E5-2660v2.yml \
  /tmp/add.c -D N 1000
                                     kerncraft                                    
/tmp/add.c                                     -m /tmp/IvyBridgeEP_E5-2660v2.yml
-D N 1000
----------------------------------- Roofline -----------------------------------
Cache or mem bound with 1 core(s)
2.02 GFLOP/s due to L1 transfer bottleneck (bw with from copy benchmark)
Arithmetic Intensity: 0.04 FLOP/B
```


.container-fluid[

.row align-items-start[

.col-6[

- Loop Kernel Analysis and Performance Modeling Toolkit
- static code analysis to infer data reuse and cache requirements

.]

.col-6[

- can infer in-core and memory bottlenecks 
- apply performance models to benchmarked data

.]

.]

.]

## Bottom Line { data-background-image="img/pacman-games.jpg" style="margin-top: -200px; background: rgba(1,21,26, 0.8); border-radius: 20px;" }

- your requirements are your guiding light in the dungeon
- reproducible ensemble based benchmarks are key


# Summary

## Take aways 

.container-fluid[

.row align-items-center[

.col-4[

![](img/balloon.jpeg){ class="figure-img img-fluid" width="100%" }

.]

.col-4[

![](img/rubber_duck_with_glasses.jpg){ class="figure-img img-fluid" width="100%" }

.]


.col-4[

![](img/pacman-games.jpg){ class="figure-img img-fluid" width="100%" }

.]

.]

.] 




.container-fluid[

.row align-items-start[

.col-4[

__Take a balloon:__

Use Tools to check the lay of the land.

.]

.col-4[

__Falsify the rubber duck:__

Profile and check your hypothesis. 

.]


.col-4[

__Survive the dungeon__

With automated ensemble based benchmarks.

.]

.]

.]



## Final Words


> *C++ is a language considered "fast".*

. . .

> We, the community, need to live up to this standard and have robust and reproducible performance numbers!

. . . 

&nbsp;

_Thank you for your attention!_



# Backup

## 

![](img/sum_of_int_vs_float.png){ class="figure-img img-fluid" width="75%" }



## Textual output, gprof

```
$ g++ -pg -O2 -std=c++11 vector_unroll_example.cpp
$ ./a.out
$ gprof ./a.out gmon.out > analysis.txt
$ head analysis.txt
Flat profile:

Each sample counts as 0.01 seconds.
  %   cumulative   self              self     total           
 time   seconds   seconds    calls  Ts/call  Ts/call  name    
 26.71      1.02     1.02                             void my_axpy<6u, vector<float>, vector<float>, vector<float> >(vector<float>&, vector<float> const&, vector<float> const&)
 26.71      2.05     1.02                             void my_axpy<2u, vector<float>, vector<float>, vector<float> >(vector<float>&, vector<float> const&, vector<float> const&)
 23.83      2.96     0.91                             void my_axpy<8u, vector<float>, vector<float>, vector<float> >(vector<float>&, vector<float> const&, vector<float> const&)
 23.04      3.84     0.88                             void my_axpy<4u, vector<float>, vector<float>, vector<float> >(vector<float>&, vector<float> const&, vector<float> const&)
  0.00      3.84     0.00        1     0.00     0.00  _GLOBAL__sub_I_main
```

Profile from [Peter Gottschling's example on vector unrolling](https://github.com/petergottschling/discovering_modern_cpp/blob/master/c%2B%2B11/vector_unroll_example.cpp).

