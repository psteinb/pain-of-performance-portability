
#include <vector>
#include <array>
#include <algorithm>
#include <random>
#include <limits>
#include <iostream>
#include <iterator>
#include <type_traits>
#include <thread>
#include <cstring>

#include "benchmark/benchmark.h"

#include "compass.hpp"



static void BM_compass_sse2(benchmark::State& state) {

  bool has_sse2 = false;

  while (state.KeepRunning()){

    benchmark::DoNotOptimize(has_sse2 = compass::runtime::has(compass::feature::sse2()));
  }


}

BENCHMARK(BM_compass_sse2);
#include "cpuinfo_x86.h"

bool cpu_features_sse2(){

  cpu_features::X86Features xi = cpu_features::GetX86Info().features;
  return xi.ssse3;
}


static void BM_cpu_features_sse2(benchmark::State& state) {

  bool has_sse2 = false;

  while (state.KeepRunning()){

    benchmark::DoNotOptimize(has_sse2 = cpu_features_sse2());
  }


}

BENCHMARK(BM_cpu_features_sse2);

BENCHMARK_MAIN();
