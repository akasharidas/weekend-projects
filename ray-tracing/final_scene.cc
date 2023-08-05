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

hittable_list random_scene() {
    hittable_list world;

    auto ground_material = make_shared<lambertian>(colour(0.5, 0.5, 0.5));
    world.add(make_shared<sphere>(point3(0, -1000, 0), 1000, ground_material));

    for (int a = -11; a < 11; a++) {
        for (int b = -11; b < 11; b++) {
            auto choose_mat = random_float();
            point3 center(a + 0.9 * random_float(), 0.2, b + 0.9 * random_float());

            if ((center - point3(4, 0.2, 0)).length() > 0.9) {
                shared_ptr<material> sphere_material;

                if (choose_mat < 0.8) {
                    // diffuse
                    auto albedo = colour::random() * colour::random();
                    sphere_material = make_shared<lambertian>(albedo);
                    world.add(make_shared<sphere>(center, 0.2, sphere_material));
                } else if (choose_mat < 0.95) {
                    // metal
                    auto albedo = colour::random(0.5, 1);
                    auto fuzz = random_float(0, 0.5);
                    sphere_material = make_shared<metal>(albedo, fuzz);
                    world.add(make_shared<sphere>(center, 0.2, sphere_material));
                } else {
                    // glass
                    sphere_material = make_shared<dielectric>(1.5);
                    world.add(make_shared<sphere>(center, 0.2, sphere_material));
                }
            }
        }
    }

    auto material1 = make_shared<dielectric>(1.5);
    world.add(make_shared<sphere>(point3(0, 1, 0), 1.0, material1));

    auto material2 = make_shared<lambertian>(colour(0.4, 0.2, 0.1));
    world.add(make_shared<sphere>(point3(-4, 1, 0), 1.0, material2));

    auto material3 = make_shared<metal>(colour(0.7, 0.6, 0.5), 0.0);
    world.add(make_shared<sphere>(point3(4, 1, 0), 1.0, material3));

    return world;
};

int main() {
    // Image dimensions
    const auto aspect_ratio = 3.0 / 2.0;
    const int width = 1000;
    const int height = int(width / aspect_ratio);
    const int samples_per_pixel = 350;
    const int max_bounces = 50;

    // Setup scene
    auto scene = random_scene();

    // Setup camera
    point3 lookfrom(13, 2, 3);
    point3 lookat(0, 0, 0);
    vec3 vup(0, 1, 0);
    auto focal_dist = 10.0;
    auto aperture = 0.1;
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