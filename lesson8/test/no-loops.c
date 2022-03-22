float func(float a, int b)
{
  float x = 42.0 / a;
  int y = 42 / b;
  return x + y;
}

int main()
{
  int a = (int)func(3.0, 3);
  return a;
}