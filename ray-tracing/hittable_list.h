#ifndef HITTABLE_LIST_H
#define HITTABLE_LIST_H

#include <memory>
#include <vector>

#include "hittable.h"
#include "ray.h"

using std::make_shared;
using std::shared_ptr;

class hittable_list : public hittable {
   public:
    std::vector<shared_ptr<hittable>> objects;

    hittable_list() {}
    hittable_list(shared_ptr<hittable> object) { add(object); }

    void add(shared_ptr<hittable> object) { objects.push_back(object); }
    void clear() { objects.clear(); }

    virtual bool hit(const ray &r, float t_min, float t_max, hit_record &rec) const override;
};

bool hittable_list::hit(const ray &r, float t_min, float t_max, hit_record &rec) const {
    auto closest_hit = t_max;
    hit_record temp_record;
    bool is_hit = false;

    for (int i = 0; i < objects.size(); i++) {
        if (objects[i]->hit(r, t_min, t_max, temp_record)) {
            is_hit = true;
            if (temp_record.t < closest_hit) {
                closest_hit = temp_record.t;
                rec = temp_record;
            }
        }
    }

    return is_hit;
}

#endif