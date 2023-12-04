# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from typing import List, NamedTuple, Optional

import spack.cmd
import spack.spec


class Request(NamedTuple):
    abstract: spack.spec.Spec
    concrete: spack.spec.Spec


def filter_specs(specs: List[spack.spec.Spec], *, installed: Optional[bool], explicit: Optional[bool]) -> List[Request]:
    """Filters the list of input specs, according to arguments.
    
    Args:
        specs: list of abstract input specs 
        installed: if True keep only specs that concretize to an installed hash, if False do 
            the opposite.
        explicit: if True keep only specs that concretize to an explicitly requested hash, if False do 
            the opposite.
    """
    specs = [Request(abstract=s, concrete=s.concretized()) for s in spack.cmd.parse_specs(specs)]

    if installed is not None:
        specs = [s for s in specs if s.concrete.installed is installed]
    
    if explicit is not None:
        specs = [s for s in specs if bool(s.concrete._installed_explicitly()) is explicit]
    
    return specs
