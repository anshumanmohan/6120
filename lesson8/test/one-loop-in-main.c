int add(int a, int b)
{
  return a + b;
}

int main()
{
  int a = 0;
  int b = 1;
  for (; a < 100;)
  {
    int c = 3 + 3;
    a = a + b;
  }
  return a;
}