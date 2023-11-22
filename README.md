Scripts used to slice and dice VCF-files during my daily work.

Some commands assumes that you have `bgzip` and `tabix` installed in your `PATH`.

Main entry point is "vtk".

I.e.:

```
vtk peek my.vcf.gz
```

How to build container:

```
sudo singularity build containers/build4.sif Singularity 
singularity exec containers/build.sif /My-VCF-tools/vtk nrec data/testout_noplugins.vcf.gz
```

Wishlist:

* Histogram