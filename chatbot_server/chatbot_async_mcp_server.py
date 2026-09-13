from fastmcp import FastMCP
import asyncio
from dotenv import load_dotenv
load_dotenv()

mcp=FastMCP(name="arith")

@mcp.tool
def as_number(x):
    #accept ints/float or numeric string otherwise raise error
    if isinstance(x,(int,float)):
        return float(x)
    if isinstance(x,str):
        return float(x.strip())
    raise TypeError("expected a number(int/float or numeric string )")

@mcp.tool
async def add(a:float,b:float)->float:
    """return a+b
    """
    return as_number(a)+as_number(b)

@mcp.tool
async def sub(a:float,b:float)->float:
    """return a-b"""
    return as_number(a)-as_number(b)

@mcp.tool
async def mul(a:float,b:float)->float:
    """return a*b
    """
    return as_number(a)*as_number(b)


@mcp.tool
async def div(a:float,b:float)->float:
    """return a/b,raises  on division by zero
    """
    a=as_number(a)
    b=as_number(b)
    if b==0:
        raise ZeroDivisionError("division by zero")
    return a/b

@mcp.tool
async def power(a:float,b:float)->float:
    """return a**b
    """
    return as_number(a)**as_number(b)

@mcp.tool
async def modulus(a:float,b:float)->float:
    """return a%b,raise division by zero"""
    a=as_number(a)
    b=as_number(b)
    if b==0:
        raise ZeroDivisionError("division by zero")
    return a%b



if __name__=="__main__":
    mcp.run()