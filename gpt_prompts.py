from langchain.prompts import PromptTemplate

examples = [
    {
        "question": """Can you help me to find the top three best cars for me?
Let's think step by step.

```
Car_index: 1
price: 6,800
mileage: 167K km
description:
2010 Honda Civic VTI, great car, has roadworthy and rego until June. Located in Crestmead 4132.
```

Car_index: 2
price: 15,000
mileage: 55K km
description:
Selling my Honda civic hatch 2019 black with very low km 56700 only.

Full logbook history services with honda only.

Comes with  safety Certificate and with almost 6 months Rego.
Car has been AMAZING! It is great on fuel and runs great, it looks amazing on the road! And beautiful colour inside and outside.. always been looked after..   Cold air-con.

Features:
Bluetooth
Screen
Reverse camera
Central locking
Cruise control
USB audio input- IPod connectivity
Storage compartment in centre console
Enjoy the ease of remote door unlocking
It would be a great car for a family, as this as served us really well! Wovi passed
Available in Acacia ridge 4110 for test drive
For more info call me or text me
```
Car_index: 3
price: 20,000
mileage: 132K km
description:
Honda civic 2020
Immaculate condition in and out of
Has no issues what so ever
Low kms
Eco mode
Open to offers
3 months rego and current Rwc
Has passed wovi inspection for minor accident got proof
Located Logan village 4207
```
Car_index: 4
price: 15,000
milage: 82K km
description:
Clear PPSR
No accident, never had issues.
Provide RWC and REGO.
OFFER welcome!
```

""",
        "answer": """
{{
"Car_index 4": "This car has a clear title and never had issues which is a good sign. When it comes to price, we can offer the best price which is another good reason.",
"Car_index 1": "This car is the cheapest of all cars. The seller did not mention it was listed on WOVR or had any accident. It can be a good deal."
}}
""",
    }
]

example_template = """
```
Question:{question}

Answer:{answer}
"""
example_prompt = PromptTemplate(input_variables=["question", "answer"], template=example_template)

prefix_conversation = """
Please act as a Australia's car dealer and be good at analyzing the context from the seller to find the best profit for your company.
You have to finish this task based on my requirements.

Task:
You are going to buy some cars, you have to find the top three best cars based on requirements.
You have to consider all the requirements factors to find a car.
When you return your final answers, please make sure it can be processed by JSON.loads().

requirements:
1. price (The cheaper, the better)
2. mileage (The lower, the better)
3. Based on the car description, check if the car was listed on the wovr or wovi or pass QIS. Just reply Yes or No.
4. If your answer in requirement 3 is 'No'. This car can be a candidate.
5. If you can not find the top 3 best cars, you can find as many as you can.
6. When you find the best cars, please tell me why you choose these cars in three sentences.

Please ALWAYS follow the requirements to accomplish the task.

Here are some examples:
"""

suffix_conversation = """
```
---
Here are real datas.
Question:{question}
Let's think step by step.

Answer:
"""
