#!/usr/bin/env python
# -*- coding: utf-8 -*-
import model



kf = model.KundFaktura()
kf.rotAvdrag1.summa = 50
kf.add_body_line(['test','','', 123.12])
kf.add_body_line(['This is a comment line'])
print kf.summa
print kf.summaExklMoms
print kf.moms