int func(int a)
{
  int x = 42 / a;
  return x;
}

int main()
{
  int a = func(3);
  return a;
}