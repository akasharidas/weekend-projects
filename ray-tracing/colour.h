#ifndef COLOUR_H
#define COLOUR_H

#include <iostream>

#include "utilities.h"

void write_colour(std::ostream &out, colour &c, int samples_per_pixel) {
    auto r = c.x();
    auto g = c.y();
    auto b = c.z();

    auto scale = 1.0 / samples_per_pixel;
    r = std::sqrt(scale * r);
    g = std::sqrt(scale * g);
    b = std::sqrt(scale * b);

    out << int(256 * clamp(r, 0.0, 0.999)) << ' '
        << int(256 * clamp(g, 0.0, 0.999)) << ' '
        << int(256 * clamp(b, 0.0, 0.999)) << '\n';
}

#endif