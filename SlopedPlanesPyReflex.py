# -*- coding: utf8 -*-
# *****************************************************************************
# *                                                                           *
# *    Copyright (c) 2017                                                     *
# *                                                                           *
# *    This program is free software; you can redistribute it and/or modify   *
# *    it under the terms of the GNU Lesser General Public License (LGPL)     *
# *    as published by the Free Software Foundation; either version 2 of      *
# *    the License, or (at your option) any later version.                    *
# *    For detail see the LICENSE text file.                                  *
# *                                                                           *
# *    This program is distributed in the hope that it will be useful,        *
# *    but WITHOUT ANY WARRANTY; without even the implied warranty of         *
# *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.                   *
# *    See the  GNU Library General Public License for more details.          *
# *                                                                           *
# *    You should have received a copy of the GNU Library General Public      *
# *    License along with this program; if not, write to the Free Software    *
# *    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307   *
# *    USA                                                                    *
# *                                                                           *
# *****************************************************************************


import Part
import SlopedPlanesUtils as utils
from SlopedPlanesPy import _Py


__title__ = "SlopedPlanes Macro"
__author__ = "Damian Caceres Moreno"
__url__ = "http://www.freecadweb.org"


class _PyReflex(_Py):

    ''''''

    def __init__(self):

        ''''''

        self.planes = []
        self.rangoInter = []

    @property
    def planes(self):

        ''''''

        return self._planes

    @planes.setter
    def planes(self, planes):

        ''''''

        self._planes = planes

    @property
    def rangoInter(self):

        ''''''

        return self._rangoInter

    @rangoInter.setter
    def rangoInter(self, rangoInter):

        ''''''

        self._rangoInter = rangoInter

    def simulating(self, tolerance):

        ''''''

        [pyR, pyOppR] = self.planes
        enormousR = pyR.enormousShape
        enormousOppR = pyOppR.enormousShape
        try:
            rCopy = pyR.simulatedShape.copy()
        except AttributeError:
            rCopy = pyR.shape.copy()
        try:
            oppRCopy = pyOppR.simulatedShape.copy()
        except AttributeError:
            oppRCopy = pyOppR.shape.copy()

        rCopy = rCopy.cut([enormousOppR], tolerance)
        gS = pyR.geom.toShape()
        rCopy = utils.selectFace(rCopy.Faces, gS, tolerance)
        pyR.simulatedShape = rCopy

        oppRCopy = oppRCopy.cut([enormousR], tolerance)
        gS = pyOppR.geom.toShape()
        oppRCopy = utils.selectFace(oppRCopy.Faces, gS, tolerance)
        pyOppR.simulatedShape = oppRCopy

    def reflexing(self, pyFace, pyWire, tolerance):

        ''''''

        pyPlaneList = self.planes

        pyR = pyPlaneList[0]
        pyOppR = pyPlaneList[1]

        pyR.oppCutter, pyR.cutter = [], []
        pyOppR.oppCutter, pyOppR.cutter = [], []

        direction = "forward"
        print '### direction ', direction
        print(pyR.numGeom, pyOppR.numGeom)

        self.twin(pyFace, pyWire, pyR, pyOppR, direction, tolerance)

        direction = "backward"
        print '### direction ', direction
        print(pyOppR.numGeom, pyR.numGeom)

        self.twin(pyFace, pyWire, pyOppR, pyR, direction, tolerance)

    def twin(self, pyFace, pyWire, pyR, pyOppR, direction, tolerance):

        ''''''

        reflexEnormous = pyR.enormousShape.copy()
        pyOppR.addLink('oppCutter', reflexEnormous)

        oppReflexEnormous = pyOppR.enormousShape

        angle = pyR.angle
        numWire = pyWire.numWire
        if ((numWire == 0 and angle > 90) or
           (numWire > 0 and angle < 90)):
            pyR.shape = pyR.simulatedShape

        pyPlaneList = pyWire.planes

        rear = pyR.rear

        for nGeom in rear:
            rearPyPl = pyPlaneList[nGeom]

            if rearPyPl.aligned:
                print 'a'
                pyAlign = pyFace.selectAlignament(numWire, nGeom)
                rearPl = pyAlign.simulatedShape
                pyOppR.addLink('oppCutter', rearPl)
                pyR.addLink('cutter', rearPl)
                print 'included rear simulated', (rearPl, numWire, nGeom)

            elif rearPyPl.choped:
                print 'b'
                rearPl = rearPyPl.simulatedShape
                pyR.addLink('cutter', rearPl)
                pyOppR.addLink('oppCutter', rearPl)
                print 'included rear simulated ', (rearPl, numWire, nGeom)

            elif rearPyPl.reflexed:
                print 'c'
                rearPl = rearPyPl.simulatedShape
                pyOppR.addLink('oppCutter', rearPl)
                pyR.addLink('cutter', rearPl)
                print 'included rear simulated', (rearPl, numWire, nGeom)

            else:
                print 'd'
                rearPl = rearPyPl.shape
                pyR.addLink('cutter', rearPl)
                pyOppR.addLink('oppCutter', rearPl)
                print 'included rear ', (rearPl, numWire, nGeom)

        oppRear = pyOppR.rear

        if len(oppRear) == 1:

            nGeom = oppRear[0]
            pyOppRear = pyPlaneList[nGeom]

            if pyOppRear.aligned:
                print 'a'
                pyAlign = pyFace.selectAlignament(numWire, nGeom)
                oppRearPl = pyAlign.simulatedShape
                pyOppR.addLink('oppCutter', oppRearPl)
                pyR.addLink('cutter', oppRearPl)
                print 'included oppRear simulated', (rearPl, numWire, nGeom)

            elif pyOppRear.choped:
                print 'b'
                oppRearPl = pyOppRear.simulatedShape
                pyR.addLink('cutter', oppRearPl)
                pyOppR.addLink('oppCutter', oppRearPl)
                print 'included oppRear simulated', (oppRearPl, numWire, nGeom)

            elif pyOppRear.reflexed:
                print 'c'
                oppRearPl = pyOppRear.simulatedShape
                pyR.addLink('cutter', oppRearPl)
                pyOppR.addLink('oppCutter', oppRearPl)
                print 'included oppRear simulated ', (oppRearPl, numWire, nGeom)

            else:
                print 'd'
                oppRearPl = pyOppRear.shape
                pyR.addLink('cutter', oppRearPl)
                pyOppR.addLink('oppCutter', oppRearPl)
                print 'included oppRear ', (oppRearPl, numWire, nGeom)

        elif len(oppRear) == 2:

            if direction == 'forward':

                self.processOppRear(oppRear, direction, pyFace, pyWire, pyR,
                                    pyOppR, oppReflexEnormous, tolerance)

            else:

                self.processOppRear(oppRear, direction, pyFace, pyWire, pyR,
                                    pyOppR, oppReflexEnormous, tolerance)

        rangoCorner = pyR.rango

        for ran in rangoCorner:
            for nn in ran:
                if nn not in oppRear:

                    self.processRango(pyFace, pyWire, pyR, pyOppR,
                                      nn, 'rangoCorner', tolerance)

        rangoNext = pyOppR.rango

        if len(rear) == 1:
            for ran in rangoNext:
                for nn in ran:

                    self.processRango(pyFace, pyWire, pyR, pyOppR,
                                      nn, 'rangoNext', tolerance)

        rangoInter = self.rangoInter
        if rangoInter:
            ran = rangoInter

            for nn in ran:

                self.processRango(pyFace, pyWire, pyR, pyOppR, nn,
                                  'rangoInter', tolerance)

    def processOppRear(self, oppRear, direction, pyFace, pyWire, pyR, pyOppR,
                       oppReflexEnormous, tolerance):

        ''''''

        nWire = pyWire.numWire

        if direction == "forward":
            nGeom = oppRear[1]
        else:
            nGeom = oppRear[0]

        pyOppRear = pyWire.planes[nGeom]
        oppRearPl = pyOppRear.shape.copy()
        pyR.addLink('cutter', oppRearPl)
        pyOppR.addLink('oppCutter', oppRearPl)
        print 'included oppRear ', (oppRearPl, nWire, nGeom)

        if direction == "forward":
            nGeom = oppRear[0]
        else:
            nGeom = oppRear[1]

        pyOppRear = pyWire.planes[nGeom]
        oppRearPl = pyOppRear.shape.copy()
        oppRearPl = oppRearPl.cut([oppReflexEnormous], tolerance)

        pointWire = pyWire.coordinates

        if direction == "forward":
            point = pointWire[nGeom+1]
        else:
            point = pointWire[nGeom]

        print 'point ', point
        vertex = Part.Vertex(point)

        for ff in oppRearPl.Faces:
            section = vertex.section([ff], tolerance)
            if section.Vertexes:
                pyR.addLink('cutter', ff)
                pyOppR.addLink('oppCutter', ff)
                print 'included oppRear rectified ', (oppRearPl, nWire, nGeom)
                break

    def processRango(self, pyFace, pyWire, pyR, pyOppR, nn, kind, tolerance):

        ''''''

        nWire = pyWire.numWire
        oppReflexEnormous = pyOppR.enormousShape
        pyPl = pyWire.planes[nn]

        if pyPl.aligned:
            print 'A'
            pyAlign = pyFace.selectAlignament(nWire, nn)
            pl = pyAlign.simulatedShape
            pyR.addLink('cutter', pl)
            pyOppR.addLink('oppCutter', pl)
            print 'included rango simulated ', (pl, nWire, nn)

        elif pyPl.choped:
            print 'B'
            pl = pyPl.simulatedShape
            pyR.addLink('cutter', pl)
            pyOppR.addLink('oppCutter', pl)
            print 'included rango simulated', (pl, nWire, nn)

        elif pyPl.reflexed:
            print 'C'

            if pyOppR.numGeom in pyPl.rear:

                pl = pyPl.simulatedShape
                pyR.addLink('cutter', pl)
                pyOppR.addLink('oppCutter', pl)
                print 'included rango simulated ', (pl, nWire, nn)

                if kind != 'rangoCorner':

                    pl = pyPl.shape.copy()
                    pl = pl.cut([oppReflexEnormous], tolerance)
                    gS = pyPl.geom.toShape()
                    pl = utils.selectFace(pl.Faces, gS, tolerance)
                    pyR.addLink('divide', pl)
                    print 'included rango divide', (pl, nWire, nn)

            else:
                pl = pyPl.simulatedShape

                if kind == 'rangoCorner':
                    print 'Corner'
                    pl = pl.cut([oppReflexEnormous], tolerance)
                    gS = pyPl.geom.toShape()
                    pl = utils.selectFace(pl.Faces, gS, tolerance)

                pyR.addLink('cutter', pl)
                pyOppR.addLink('oppCutter', pl)
                print 'included rango simulated ', (pl, nWire, nn)

        else:
            print 'D'
            pl = pyPl.shape.copy()

            if kind == 'rangoCorner':
                print 'rangoCorner'
                pl = pl.cut([oppReflexEnormous], tolerance)
                gS = pyPl.geom.toShape()
                pl = utils.selectFace(pl.Faces, gS, tolerance)

            pyR.addLink('cutter', pl)
            pyOppR.addLink('oppCutter', pl)
            print 'included rango ', (pl, nWire, nn)

    def solveReflex(self, face, tolerance):

        ''''''


        [pyR, pyOppR] = self.planes
        # print(pyR.numGeom, pyOppR.numGeom)
        reflex = pyR.shape.copy()
        oppReflex = pyOppR.shape.copy()

        self.processReflex(reflex, oppReflex,
                           pyR, pyOppR, face,
                           'forward', tolerance)

        self.processReflex(oppReflex, reflex,
                           pyOppR, pyR, face,
                           'backward', tolerance)

    def processReflex(self, reflex, oppReflex, pyR, pyOppR, face,
                      direction, tolerance):

        ''''''

        numWire = pyR.numWire

        aa = reflex.copy()
        bb = oppReflex.copy()

        divide = pyR.divide

        bb = bb.cut(pyOppR.oppCutter + divide, tolerance)
        gS = pyOppR.geom.toShape()
        if len(pyOppR.rear) == 1:
            if numWire == 0:
                vertex = pyOppR.forward.firstVertex(True)
            else:
                vertex = pyOppR.backward.firstVertex(True)
        else:
            if direction == 'backward':
                vertex = pyOppR.forward.firstVertex(True)
            else:
                vertex = pyOppR.backward.firstVertex(True)
        # print vertex.Point

        for ff in bb.Faces:
            section = ff.section([gS], tolerance)
            if section.Edges:
                section = ff.section([vertex], tolerance)
                if section.Vertexes:
                    bb = ff
                    # print 'a'
                    break

        aa = aa.cut(pyR.cutter+[bb], tolerance)

        aList = []
        gS = pyR.geom.toShape()
        AA = utils.selectFace(aa.Faces, gS, tolerance)
        aList.append(AA)
        aa = aa.removeShape([AA])

        forward = pyR.forward
        backward = pyR.backward

        rear = pyR.cutter[0]
        if len(pyOppR.rear) == 1:
            oppRear = pyOppR.cutter[0]
            try:
                firstRangoCorner = pyR.cutter[2]
            except IndexError:
                pass
        else:
            firstRangoCorner = pyR.cutter[3]
            if direction == 'forward':
                oppRear = pyOppR.cutter[1]
            else:
                oppRear = pyOppR.cutter[0]

        if aa.Faces:

            oppReflexEnormous = pyOppR.enormousShape
            aa = aa.cut(divide + [oppReflexEnormous], tolerance)

            under = []
            for ff in aa.Faces:
                # print 'aa'
                section = ff.section([face], tolerance)
                if section.Edges:
                    # print 'bb'
                    section = ff.section([rear], tolerance)
                    if section.Edges:
                        # print 'cc'
                        aa = aa.removeShape([ff])
                        under.append(ff)
                        ### break

            if under:
                for ff in aa.Faces:
                    # print 'a'
                    section = ff.section([face], tolerance)
                    if not section.Edges:
                        # print 'b'
                        section = ff.section(under, tolerance)
                        if section.Edges:
                            # print 'c'
                            section = ff.section([AA], tolerance)
                            if not section.Edges:
                                # print 'd'
                                section = ff.section([forward, backward],
                                                     tolerance)
                                if not section.Edges:
                                    # print 'e'
                                    section = ff.section([rear], tolerance)
                                    if section.Edges:
                                        # print 'f'
                                        section = ff.section([oppRear],
                                                             tolerance)
                                        if not section.Edges:
                                            # print 'g'
                                            section =\
                                                ff.section([firstRangoCorner],
                                                           tolerance)
                                            if section.Vertexes:
                                                # print 'h'
                                                aList.append(ff)
                                                break

        compound = Part.makeCompound(aList)
        if pyR.compound:
            compound = Part.makeCompound([compound, pyR.compound])
        else:
            pyR.compound = compound

    def rearReflex(self, pyWire, tolerance):

        ''''''

        pyPlaneList = pyWire.planes

        for pyPlane in self.planes:
            if len(pyPlane.compound.Faces) > 1:
                rear = pyPlane.rear
                for nGeom in rear:
                    pyRear = pyPlaneList[nGeom]
                    if pyRear.reflexed:
                        # print 'rearReflex'
                        # print pyRear.numGeom
                        rearPl = pyRear.compound
                        rearPl = rearPl.cut([pyPlane.compound], tolerance)
                        gS = pyRear.geom.toShape()
                        rearPl = utils.selectFace(rearPl.Faces, gS, tolerance)
                        pyRear.compound = rearPl

                        # TODO aplica tambien al oppReflex de rearPl

    def compounding(self, tolerance):

        ''''''

        [pyR, pyOppR] = self.planes

        compoundA = pyR.compound
        compoundB = pyOppR.compound

        lenA = len(compoundA.Faces)
        lenB = len(compoundB.Faces)

        # print lenA
        # print lenB

        if lenB > 1 and lenA == 1:
            # print 'A'
            compoundA = compoundA.cut([compoundB], tolerance)
            gS = pyR.geom.toShape()
            compoundA = utils.selectFace(compoundA.Faces, gS, tolerance)

        elif lenA > 1 and lenB == 1:
            # print 'B'
            compoundB = compoundB.cut([compoundA], tolerance)
            gS = pyOppR.geom.toShape()
            compoundB = utils.selectFace(compoundB.Faces, gS, tolerance)

        elif lenA == 1 and lenB == 1:
            # print 'C'
            # TODO make copy
            compoundA = compoundA.cut([compoundB], tolerance)
            gS = pyR.geom.toShape()
            compoundA = utils.selectFace(compoundA.Faces, gS, tolerance)

            compoundB = compoundB.cut([compoundA], tolerance)
            gS = pyOppR.geom.toShape()
            compoundB = utils.selectFace(compoundB.Faces, gS, tolerance)

        else:
            # print 'D'
            pass

        pyR.shape = compoundA
        pyOppR.shape = compoundB

    def reviewing(self, tolerance):

        ''''''

        for pyPlane in self.planes:
            pyPlane.isSolved(tolerance)

    def rearing(self, pyWire, tolerance):

        ''''''

        for pyPlane in self.planes:
            if not pyPlane.reflexed:
                pyPlane.rearing(pyWire, self, tolerance)

    def rangging(self, pyWire):

        ''''''

        lenWire = len(pyWire.planes)

        rear = self.planes[0].rear
        oppRear = self.planes[1].rear

        rG = rear[0]
        try:
            oG = oppRear[1]
        except IndexError:
            oG = oppRear[0]

        if oG > rG:
            # print '1'
            ran = range(rG+1, oG)

        elif oG < rG:
            # print '2'
            ranA = range(rG+1, lenWire)
            ranB = range(0, oG)
            ran = ranA + ranB

        else:
            # print '3'
            ran = []

        # print 'rangoInter ', ran

        self.rangoInter = ran
