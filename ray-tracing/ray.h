#ifndef RAY_H
#define RAY_H

#include <iostream>

#include "vec3.h"

class ray {
   public:
    point3 origin;
    vec3 direction;

    ray() {}
    ray(const point3 &orig, const vec3 &dir) : origin(orig), direction(dir) {}

    point3 at(float t) const {
        return origin + t * direction;
    }
};

#endif