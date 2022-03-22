int add(int a, int b)
{
  return a + b;
}

int main()
{
  int a = 0;
  for (; a < 100;)
  {
    int b = add(3, 3);
    a = a + b;
  }
  return a;
}