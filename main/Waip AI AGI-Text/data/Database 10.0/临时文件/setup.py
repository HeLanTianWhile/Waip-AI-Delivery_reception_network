from setuptools import setup, Extension

ext = Extension(
    "Waip_AI_DRN_0_1_3",
    sources=["Waip AI DRN 0.1.3.cpp"],
    language="c++",
)

setup(
    name="Waip_AI_DRN_0_1_3",
    ext_modules=[ext],
)
