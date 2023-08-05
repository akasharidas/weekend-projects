#include <iostream>

#include "camera.h"
#include "colour.h"
#include "hittable_list.h"
#include "material.h"
#include "sphere.h"
#include "utilities.h"

// Blue gradient background
colour ray_colour(const ray &r, const hittable &scene, int depth) {
    if (depth <= 0)
        return colour(0, 0, 0);

    hit_record rec;

    if (scene.hit(r, 0.001, infinity, rec)) {
        ray scattered;
        colour attenuation;

        if (rec.mat_ptr->scatter(r, rec, attenuation, scattered))
            return attenuation * ray_colour(scattered, scene, depth - 1);
        return colour(0, 0, 0);
    }

    vec3 unit_direction = unit_vector(r.direction);
    auto t = 0.5 * (unit_direction.y() + 1.0);
    return (1.0 - t) * colour(1.0, 1.0, 1.0) + t * colour(0.5, 0.7, 1.0);
}

int main() {
    // Image dimensions
    const auto aspect_ratio = 16.0 / 9.0;
    const int height = 512;
    const int width = int(aspect_ratio * height);
    const int samples_per_pixel = 100;
    const int max_bounces = 50;

    // Setup scene
    hittable_list scene;

    colour earth_brown = colour(112.0 / 256, 72.0 / 256, 60.0 / 256) * 1.2;
    auto material_ground = make_shared<lambertian>(earth_brown);
    auto material_diffuse = make_shared<lambertian>(colour(1, 0.2, 0.2));
    auto material_metal1 = make_shared<metal>(colour(0.8, 0.8, 0.8), 0);
    auto material_dielectric = make_shared<dielectric>(1.5);

    scene.add(make_shared<sphere>(point3(1, 0, -1), 0.5, material_diffuse));
    scene.add(make_shared<sphere>(point3(0, 0, -1), 0.5, material_dielectric));
    scene.add(make_shared<sphere>(point3(0, 0, -1), -0.49, material_dielectric));
    scene.add(make_shared<sphere>(point3(-1, 0, -1), 0.5, material_metal1));
    scene.add(make_shared<sphere>(point3(-1, -0.5 + 1.0 / 16, -1 + 0.75), 1.0 / 16, material_diffuse));
    scene.add(make_shared<sphere>(point3(-1 - 0.75, -0.5 + 1.0 / 16, -1), 1.0 / 16, material_diffuse));

    scene.add(make_shared<sphere>(point3(0, -100.5, -1), 100, material_ground));

    point3 lookfrom = point3(-5, 0.5, 0.75);
    point3 lookat = point3(1, -0.25, -1);  // Look at far ball
    vec3 vup(0, 1, 0);
    float aperture = 0.1;
    float focal_dist = (point3(-1, 0, -1) - lookfrom).length();  // Focus on near ball

    // Setup camera
    camera cam(lookfrom, lookat, vup, 20.0, aspect_ratio, aperture, focal_dist);

    // Render image
    std::cout << "P3\n"
              << width << ' ' << height << "\n255\n";

    for (int i = height - 1; i > 0; i--) {
        std::cerr << "\rRows remaining: " << i << ' ' << std::flush;

        for (int j = 0; j < width; j++) {
            colour pixel(0, 0, 0);

            for (int s = 0; s < samples_per_pixel; s++) {
                float offset_x = (j + random_float()) / (width - 1);
                float offset_y = (i + random_float()) / (height - 1);
                pixel += ray_colour(cam.get_ray(offset_x, offset_y), scene, max_bounces);
            }

            write_colour(std::cout, pixel, samples_per_pixel);
        }
    }
}