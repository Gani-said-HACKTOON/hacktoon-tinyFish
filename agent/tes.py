from dotenv import load_dotenv
load_dotenv()

from tinyfish import TinyFish

client = TinyFish()

run_id = None

with client.agent.stream(
    url="https://peraturan.bpk.go.id",
    goal="Sebutkan 3 regulasi terbaru. Jawab 2 kalimat saja."
) as stream:
    for event in stream:
        ev = event.type.value if hasattr(event.type, "value") else str(event.type)
        print(f"[{ev}]")
        if ev == "COMPLETE":
            run_id = event.run_id
            print(f"run_id: {run_id}")
            break

# Coba fetch hasil pakai run_id
print("\n--- COBA FETCH HASIL ---")
try:
    result = client.runs.get(run_id)
    print(f"type: {type(result)}")
    print(f"value: {result}")
    for attr in dir(result):
        if not attr.startswith('_'):
            try:
                val = getattr(result, attr)
                if not callable(val):
                    print(f"{attr} = {str(val)[:300]}")
            except:
                pass
except Exception as e:
    print(f"Error: {e}")