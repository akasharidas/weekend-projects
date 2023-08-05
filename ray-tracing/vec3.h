#ifndef VEC3_H
#define VEC3_H

#include <cmath>
#include <iostream>

#include "utilities.h"

class vec3 {
   public:
    float e[3];

    vec3(float x = 0, float y = 0, float z = 0) : e{x, y, z} {}

    float x() { return e[0]; }
    float y() { return e[1]; }
    float z() { return e[2]; }

    // negate
    vec3 operator-() const { return vec3(-e[0], -e[1], -e[2]); }

    // this one allows you access an element as a copy, like a = vec[0]
    float operator[](int i) const { return e[i]; }
    // this one allows you to set an element, like vec[0] = 2
    float &operator[](int i) { return e[i]; }

    // +=
    vec3 &operator+=(const vec3 &other) {
        e[0] += other.e[0];
        e[1] += other.e[1];
        e[2] += other.e[2];
        return *this;
    }
    vec3 &operator+=(const float a) {
        e[0] += a;
        e[1] += a;
        e[2] += a;
        return *this;
    }

    // *=
    vec3 &operator*=(const float a) {
        e[0] *= a;
        e[1] *= a;
        e[2] *= a;
        return *this;
    }

    // /=
    vec3 &operator/=(const float a) {
        e[0] *= a;
        e[1] *= a;
        e[2] *= a;
        return *this;
    }

    // length
    float length() const {
        return std::sqrt(length_squared());
    }
    float length_squared() const {
        return e[0] * e[0] + e[1] * e[1] + e[2] * e[2];
    }

    inline static vec3 random() {
        return vec3(random_float(), random_float(), random_float());
    }

    inline static vec3 random(float min, float max) {
        return vec3(random_float(min, max), random_float(min, max), random_float(min, max));
    }

    bool near_zero() const {
        const auto s = 1e-8;
        return (fabs(e[0]) < s) && (fabs(e[1]) < s) && (fabs(e[2]) < s);
    }
};

// alias for vec3 - point3 and color
using point3 = vec3;
using colour = vec3;

// like python __repr__
inline std::ostream &operator<<(std::ostream &out, const vec3 &v) {
    return out << v.e[0] << ' ' << v.e[1] << ' ' << v.e[2];
}

inline vec3 operator+(const vec3 &a, const vec3 &b) {
    return vec3(a.e[0] + b.e[0], a.e[1] + b.e[1], a.e[2] + b.e[2]);
}

inline vec3 operator-(const vec3 &a, const vec3 &b) {
    return vec3(a.e[0] - b.e[0], a.e[1] - b.e[1], a.e[2] - b.e[2]);
}

inline vec3 operator*(const vec3 &a, const vec3 &b) {
    return vec3(a.e[0] * b.e[0], a.e[1] * b.e[1], a.e[2] * b.e[2]);
}

inline vec3 operator*(float a, const vec3 &vec) {
    return vec3(a * vec.e[0], a * vec.e[1], a * vec.e[2]);
}

inline vec3 operator*(const vec3 &vec, float a) {
    return a * vec;
}

inline vec3 operator/(vec3 vec, double a) {
    return (1 / a) * vec;
}

inline float dot(const vec3 &a, const vec3 &b) {
    return a.e[0] * b.e[0] + a.e[1] * b.e[1] + a.e[2] * b.e[2];
}

inline vec3 cross(const vec3 &a, const vec3 &b) {
    return vec3(a.e[1] * b.e[2] - a.e[2] * b.e[1],
                a.e[2] * b.e[0] - a.e[0] * b.e[2],
                a.e[0] * b.e[1] - a.e[1] * b.e[0]);
}

inline vec3 unit_vector(const vec3 &a) {
    return a / a.length();
}

vec3 random_in_unit_sphere() {
    while (true) {
        vec3 p = vec3::random(-1, 1);
        if (p.length_squared() >= 1) continue;
        return p;
    }
}

vec3 random_in_unit_disk() {
    while (true) {
        vec3 p = vec3(random_float(-1, 1), random_float(-1, 1), 0);
        if (p.length_squared() >= 1) continue;
        return p;
    }
}

vec3 random_unit_sphere() {
    return unit_vector(random_in_unit_sphere());
}

vec3 reflect(const vec3 &v, const vec3 &n) {
    return v - 2 * dot(v, n) * n;
}

vec3 refract(const vec3 &uv, const vec3 &n, double etai_over_etat) {
    auto cos_theta = fmin(dot(-uv, n), 1.0);
    vec3 r_out_perp = etai_over_etat * (uv + cos_theta * n);
    vec3 r_out_parallel = -sqrt(fabs(1.0 - r_out_perp.length_squared())) * n;
    return r_out_perp + r_out_parallel;
}

#endif