#ifndef HITTABLE_H
#define HITTABLE_H

#include "ray.h"
#include "utilities.h"
class material;

struct hit_record {
    point3 p;
    vec3 normal;
    float t;
    shared_ptr<material> mat_ptr;
    bool front_face;

    inline void set_front_face(const ray &r, const vec3 &outward_normal) {
        front_face = (dot(r.direction, outward_normal) < 0);
        normal = front_face ? outward_normal : -outward_normal;
    }
};

class hittable {
   public:
    virtual bool hit(const ray &ray, float t_min, float t_max, hit_record &rec) const = 0;
};

#endif