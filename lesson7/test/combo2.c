float func(int a, float b)
{
  int x = 42 / a;
  float y = 42.0 / b;
  return x + y;
}

int main()
{
  int a = (int)func(3, 3.0);
  return a;
}