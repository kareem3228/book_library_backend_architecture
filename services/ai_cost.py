def account_costs(input_tokens:int,output_tokens:int,input_price:float,output_price:float):
    input_cost=input_tokens/1000000 * input_price
    output_cost=output_tokens/1000000 *output_price
    return input_cost+output_cost