#ifndef CAMERA_H
#define CAMERA_H

#include "utilities.h"

class camera {
   public:
    camera(point3 lookfrom,
           point3 lookat,
           vec3 vup,
           float vfov,
           float aspect_ratio,
           float aperture,
           float focal_dist) {
        auto theta = degrees_to_radians(vfov);
        auto h = tan(theta / 2);

        auto viewport_height = 2.0 * h;
        auto viewport_width = aspect_ratio * viewport_height;

        w = unit_vector(lookfrom - lookat);
        u = unit_vector(cross(vup, w));
        v = cross(w, u);

        lens_radius = aperture / 2;
        origin = lookfrom;
        horizontal = u * viewport_width * focal_dist;
        vertical = v * viewport_height * focal_dist;
        lower_left = origin - horizontal / 2 - vertical / 2 - w * focal_dist;
    }

    ray get_ray(float offset_x, float offset_y) const {
        vec3 lens_offset = lens_radius * random_in_unit_disk();
        vec3 offset_vector = u * lens_offset.x() + v * lens_offset.y();

        return ray(origin + offset_vector, lower_left + offset_x * horizontal + offset_y * vertical - origin - offset_vector);
    }

   private:
    point3 origin;
    vec3 horizontal;
    vec3 vertical;
    point3 lower_left;
    vec3 u, v, w;
    float lens_radius;
};

#endif