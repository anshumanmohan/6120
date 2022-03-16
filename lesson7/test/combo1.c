float func()
{
  float x = 42.0 / 3.0;
  int y = 42 / 3;
  return x + y;
}

int main()
{
  int a = (int)func();
  return a;
}