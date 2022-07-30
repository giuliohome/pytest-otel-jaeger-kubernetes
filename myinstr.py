import sys
from random import randint
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.trace.status import Status, StatusCode


otel_collector_url = sys.argv[1] 
mymsg = sys.argv[2] 

otlp_exporter = OTLPSpanExporter(endpoint=otel_collector_url, insecure=True)  
resource = Resource(attributes={
    "service.name": "service-pyshell"
})

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))
tracer = trace.get_tracer("pyshell")

def roll(sides, rolls):
     with tracer.start_as_current_span("test_case_ABC_"+mymsg, kind = trace.SpanKind(1)) as span:
         span.set_attribute("url", "myurl1")
         trace_id = span.get_span_context().trace_id
         print("trace id:", f"{trace_id:x}" )
         with tracer.start_as_current_span("test_step_123_"+mymsg) as span1:
           r = roll_sum(sides,rolls,span1)	
         span.set_status(Status(status_code=StatusCode.OK))
         return r

def roll_sum(sides, rolls, child):
    span = child
    sum = 0
    for r in range(0,rolls):
        result = randint(1,sides)
        span.add_event( "log", {
            "roll.sides": sides,
            "roll.result": result,
        })
        sum += result
    span.set_status(Status(status_code=StatusCode.OK))
    return  str(sum)

roll(10,2)



