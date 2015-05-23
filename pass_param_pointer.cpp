// g++ --std=c++11 pass_param_pointer.cpp                                                                                                                                   
// ./a.out                                                                                                                                                 
#include <iostream>
#include <memory>

class DBInterface {
public:
  virtual int GetId() const = 0;
};

class Filter {
public:
  explicit Filter(const DBInterface& db) : db_(db) {
  }

  int Output() const {
    return db_.GetId();
  }

private:
  const DBInterface& db_;  // not owned.                                                                                                                   
};

class Param {
public:
  Param() : filter_(nullptr) {}
  virtual ~Param() {}

  const Filter* filter() {
    return filter_.get();
  }

  void set_filter(std::unique_ptr<Filter>* filter) {
    filter_ = std::move(*filter);
  }

private:
  std::unique_ptr<Filter> filter_;  // Owned                                                                                                               
};

class Datastore : public DBInterface {
public:
  Datastore() {}

  int GetId() const override { return 10; }

  void DoFilter(Param* param) {
    std::unique_ptr<Filter> filter(new Filter(*this));
    param->set_filter(&filter);
  }
};

int main() {
  Param param;
  if (param.filter() == nullptr) {
    std::cout << "param.filter() is nullptr\n";
  }
  Datastore d;
  d.DoFilter(&param);
  std::cout << param.filter()->Output() << std::endl;
}
