int func(int a, int b)
{
  while (a > b)
  {
    a = a - b;
  }
  return a;
}

int main()
{
  int a = 0;
  for (; a < 100;)
  {
    int b = func(4, 3);
    a = a + b;
  }
  for (; 0 < a; a--)
  {
  }
  return a;
}