#ifndef MATERIAL_H
#define MATERIAL_H

#include "hittable.h"
#include "utilities.h"

struct hit_record;

class material {
   public:
    virtual bool scatter(const ray &ray_in, const hit_record &rec, colour &attentuation, ray &scattered) const = 0;
};

class lambertian : public material {
   public:
    colour albedo;

    lambertian(const colour &c) : albedo(c) {}

    virtual bool scatter(const ray &ray_in, const hit_record &rec, colour &attentuation, ray &scattered) const override {
        auto scatter_direction = rec.normal + random_unit_sphere();
        scattered = ray(rec.p, scatter_direction);

        if (scatter_direction.near_zero())
            scatter_direction = rec.normal;

        attentuation = albedo;
        return true;
    }
};

class metal : public material {
   public:
    colour albedo;
    float fuzz;

    metal(const colour &c, float f) : albedo(c), fuzz(f < 1 ? f : 1) {}

    virtual bool scatter(const ray &ray_in, const hit_record &rec, colour &attenuation, ray &scattered) const override {
        scattered = ray(rec.p, reflect(unit_vector(ray_in.direction), rec.normal) + fuzz * random_in_unit_sphere());
        attenuation = albedo;
        return (dot(scattered.direction, rec.normal) > 0);
    }
};

class dielectric : public material {
   public:
    float ir;

    dielectric(float i) : ir(i) {}

    virtual bool scatter(const ray &ray_in, const hit_record &rec, colour &attenuation, ray &scattered) const override {
        float refraction_ratio = rec.front_face ? (1.0 / ir) : ir;

        auto unit_direction = unit_vector(ray_in.direction);
        auto cos_theta = fmin(dot(-unit_direction, rec.normal), 1.0);
        auto sin_theta = std::sqrt(1 - cos_theta * cos_theta);

        bool cannot_refract = refraction_ratio * sin_theta > 1.0;

        vec3 direction;

        if (cannot_refract || reflectance(cos_theta, refraction_ratio) > random_float())
            direction = reflect(unit_direction, rec.normal);
        else
            direction = refract(unit_direction, rec.normal, refraction_ratio);

        scattered = ray(rec.p, direction);
        attenuation = colour(1.0, 1.0, 1.0);
        return true;
    }

   private:
    static double reflectance(double cosine, double ref_idx) {
        // Use Schlick's approximation for reflectance.
        auto r0 = (1 - ref_idx) / (1 + ref_idx);
        r0 = r0 * r0;
        return r0 + (1 - r0) * pow((1 - cosine), 5);
    }
};

#endif