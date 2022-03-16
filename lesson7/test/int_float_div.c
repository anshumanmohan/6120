float func(float a)
{
  float x = 42 / a;
  return x;
}

int main()
{
  int a = (int)func(3.0);
  return a;
}