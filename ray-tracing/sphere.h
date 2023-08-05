#ifndef SPHERE_H
#define SPHERE_H

#include "hittable.h"

class sphere : public hittable {
   public:
    point3 center;
    float radius;
    shared_ptr<material> mat_ptr;

    sphere() {}
    sphere(point3 cen, float r, shared_ptr<material> mat) : center(cen), radius(r), mat_ptr(mat){};

    virtual bool hit(const ray &r, float t_min, float t_max, hit_record &rec) const override;
};

bool sphere::hit(const ray &r, float t_min, float t_max, hit_record &rec) const {
    vec3 ac = r.origin - center;

    float a = r.direction.length_squared();
    float half_b = dot(r.direction, ac);
    float c = ac.length_squared() - radius * radius;
    float discriminant = half_b * half_b - a * c;

    if (discriminant < 0)
        return false;

    auto sqrt_discriminant = std::sqrt(discriminant);

    auto dist = (-half_b - sqrt_discriminant) / a;
    if (dist < t_min || dist > t_max) {
        dist = (-half_b + sqrt_discriminant) / a;
        if (dist < t_min || dist > t_max)
            return false;
    }

    rec.t = dist;
    rec.p = r.at(dist);
    auto outward_normal = (rec.p - center) / radius;
    rec.set_front_face(r, outward_normal);
    rec.mat_ptr = mat_ptr;

    return true;
}

#endif