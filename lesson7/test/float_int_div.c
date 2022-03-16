float func(int a)
{
  float x = 42.0 / a;
  return x;
}

int main()
{
  int a = (int)func(3);
  return a;
}