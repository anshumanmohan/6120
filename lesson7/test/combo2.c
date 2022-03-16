float func()
{
  int x = 42 / 3;
  float y = 42.0 / 3.0;
  return x + y;
}

int main()
{
  int a = (int)func();
  return a;
}