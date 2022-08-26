import sys
from random import randint
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
# you can switch the comment to select grpc protocol on (fw)port (2)4317 or http on (fw)port (2)4318
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
# from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.trace.status import Status, StatusCode


otel_collector_url = sys.argv[1] # "localhost:24317" 

service_name = "pyshell"
otlp_exporter = OTLPSpanExporter(endpoint=otel_collector_url, insecure=True) # only for grpc: , insecure=True)  
resource = Resource(attributes={
    "service.name": service_name
})

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))
tracer = trace.get_tracer(service_name)

a=tracer.start_span('DistributedTestTrace')
a.context
# SpanContext(trace_id=0x94f61d7bd16071fb6d826ccfefec5c83, span_id=0x6947945713d7c017, trace_flags=0x01, trace_state=[], is_remote=False)
from opentelemetry.trace.propagation import set_span_in_context
ctx = set_span_in_context(a)
ctx
# {'current-span-6e6e35f7-bc0b-4ec9-84f0-7af5b96ec769': _Span(name="first", context=SpanContext(trace_id=0x94f61d7bd16071fb6d826ccfefec5c83, span_id=0x6947945713d7c017, trace_flags=0x01, trace_state=[], is_remote=False))}
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
prop = TraceContextTextMapPropagator()
carrier = {}
a.end()
prop.inject(carrier=carrier,context=ctx)
carrier
print(carrier['traceparent'])
