
bomb:     file format elf32-i386


Disassembly of section .init:

08048540 <_init>:
 8048540:	53                   	push   %ebx
 8048541:	83 ec 08             	sub    $0x8,%esp
 8048544:	e8 97 01 00 00       	call   80486e0 <__x86.get_pc_thunk.bx>
 8048549:	81 c3 b7 3a 00 00    	add    $0x3ab7,%ebx
 804854f:	8b 83 fc ff ff ff    	mov    -0x4(%ebx),%eax
 8048555:	85 c0                	test   %eax,%eax
 8048557:	74 05                	je     804855e <_init+0x1e>
 8048559:	e8 22 01 00 00       	call   8048680 <__gmon_start__@plt>
 804855e:	83 c4 08             	add    $0x8,%esp
 8048561:	5b                   	pop    %ebx
 8048562:	c3                   	ret

Disassembly of section .plt:

08048570 <.plt>:
 8048570:	ff 35 04 c0 04 08    	push   0x804c004
 8048576:	ff 25 08 c0 04 08    	jmp    *0x804c008
 804857c:	00 00                	add    %al,(%eax)
	...

08048580 <printf@plt>:
 8048580:	ff 25 0c c0 04 08    	jmp    *0x804c00c
 8048586:	68 00 00 00 00       	push   $0x0
 804858b:	e9 e0 ff ff ff       	jmp    8048570 <.plt>

08048590 <fflush@plt>:
 8048590:	ff 25 10 c0 04 08    	jmp    *0x804c010
 8048596:	68 08 00 00 00       	push   $0x8
 804859b:	e9 d0 ff ff ff       	jmp    8048570 <.plt>

080485a0 <fgets@plt>:
 80485a0:	ff 25 14 c0 04 08    	jmp    *0x804c014
 80485a6:	68 10 00 00 00       	push   $0x10
 80485ab:	e9 c0 ff ff ff       	jmp    8048570 <.plt>

080485b0 <signal@plt>:
 80485b0:	ff 25 18 c0 04 08    	jmp    *0x804c018
 80485b6:	68 18 00 00 00       	push   $0x18
 80485bb:	e9 b0 ff ff ff       	jmp    8048570 <.plt>

080485c0 <sleep@plt>:
 80485c0:	ff 25 1c c0 04 08    	jmp    *0x804c01c
 80485c6:	68 20 00 00 00       	push   $0x20
 80485cb:	e9 a0 ff ff ff       	jmp    8048570 <.plt>

080485d0 <__stack_chk_fail@plt>:
 80485d0:	ff 25 20 c0 04 08    	jmp    *0x804c020
 80485d6:	68 28 00 00 00       	push   $0x28
 80485db:	e9 90 ff ff ff       	jmp    8048570 <.plt>

080485e0 <getenv@plt>:
 80485e0:	ff 25 24 c0 04 08    	jmp    *0x804c024
 80485e6:	68 30 00 00 00       	push   $0x30
 80485eb:	e9 80 ff ff ff       	jmp    8048570 <.plt>

080485f0 <puts@plt>:
 80485f0:	ff 25 28 c0 04 08    	jmp    *0x804c028
 80485f6:	68 38 00 00 00       	push   $0x38
 80485fb:	e9 70 ff ff ff       	jmp    8048570 <.plt>

08048600 <exit@plt>:
 8048600:	ff 25 2c c0 04 08    	jmp    *0x804c02c
 8048606:	68 40 00 00 00       	push   $0x40
 804860b:	e9 60 ff ff ff       	jmp    8048570 <.plt>

08048610 <strlen@plt>:
 8048610:	ff 25 30 c0 04 08    	jmp    *0x804c030
 8048616:	68 48 00 00 00       	push   $0x48
 804861b:	e9 50 ff ff ff       	jmp    8048570 <.plt>

08048620 <__libc_start_main@plt>:
 8048620:	ff 25 34 c0 04 08    	jmp    *0x804c034
 8048626:	68 50 00 00 00       	push   $0x50
 804862b:	e9 40 ff ff ff       	jmp    8048570 <.plt>

08048630 <__isoc99_sscanf@plt>:
 8048630:	ff 25 38 c0 04 08    	jmp    *0x804c038
 8048636:	68 58 00 00 00       	push   $0x58
 804863b:	e9 30 ff ff ff       	jmp    8048570 <.plt>

08048640 <fopen@plt>:
 8048640:	ff 25 3c c0 04 08    	jmp    *0x804c03c
 8048646:	68 60 00 00 00       	push   $0x60
 804864b:	e9 20 ff ff ff       	jmp    8048570 <.plt>

08048650 <strtok@plt>:
 8048650:	ff 25 40 c0 04 08    	jmp    *0x804c040
 8048656:	68 68 00 00 00       	push   $0x68
 804865b:	e9 10 ff ff ff       	jmp    8048570 <.plt>

08048660 <atoi@plt>:
 8048660:	ff 25 44 c0 04 08    	jmp    *0x804c044
 8048666:	68 70 00 00 00       	push   $0x70
 804866b:	e9 00 ff ff ff       	jmp    8048570 <.plt>

08048670 <__ctype_b_loc@plt>:
 8048670:	ff 25 48 c0 04 08    	jmp    *0x804c048
 8048676:	68 78 00 00 00       	push   $0x78
 804867b:	e9 f0 fe ff ff       	jmp    8048570 <.plt>

Disassembly of section .plt.got:

08048680 <__gmon_start__@plt>:
 8048680:	ff 25 fc bf 04 08    	jmp    *0x804bffc
 8048686:	66 90                	xchg   %ax,%ax

Disassembly of section .text:

08048690 <_start>:
 8048690:	31 ed                	xor    %ebp,%ebp
 8048692:	5e                   	pop    %esi
 8048693:	89 e1                	mov    %esp,%ecx
 8048695:	83 e4 f0             	and    $0xfffffff0,%esp
 8048698:	50                   	push   %eax
 8048699:	54                   	push   %esp
 804869a:	52                   	push   %edx
 804869b:	e8 23 00 00 00       	call   80486c3 <_start+0x33>
 80486a0:	81 c3 60 39 00 00    	add    $0x3960,%ebx
 80486a6:	8d 83 30 d6 ff ff    	lea    -0x29d0(%ebx),%eax
 80486ac:	50                   	push   %eax
 80486ad:	8d 83 d0 d5 ff ff    	lea    -0x2a30(%ebx),%eax
 80486b3:	50                   	push   %eax
 80486b4:	51                   	push   %ecx
 80486b5:	56                   	push   %esi
 80486b6:	c7 c0 a6 87 04 08    	mov    $0x80487a6,%eax
 80486bc:	50                   	push   %eax
 80486bd:	e8 5e ff ff ff       	call   8048620 <__libc_start_main@plt>
 80486c2:	f4                   	hlt
 80486c3:	8b 1c 24             	mov    (%esp),%ebx
 80486c6:	c3                   	ret
 80486c7:	66 90                	xchg   %ax,%ax
 80486c9:	66 90                	xchg   %ax,%ax
 80486cb:	66 90                	xchg   %ax,%ax
 80486cd:	66 90                	xchg   %ax,%ax
 80486cf:	90                   	nop

080486d0 <_dl_relocate_static_pie>:
 80486d0:	f3 c3                	repz ret
 80486d2:	66 90                	xchg   %ax,%ax
 80486d4:	66 90                	xchg   %ax,%ax
 80486d6:	66 90                	xchg   %ax,%ax
 80486d8:	66 90                	xchg   %ax,%ax
 80486da:	66 90                	xchg   %ax,%ax
 80486dc:	66 90                	xchg   %ax,%ax
 80486de:	66 90                	xchg   %ax,%ax

080486e0 <__x86.get_pc_thunk.bx>:
 80486e0:	8b 1c 24             	mov    (%esp),%ebx
 80486e3:	c3                   	ret
 80486e4:	66 90                	xchg   %ax,%ax
 80486e6:	66 90                	xchg   %ax,%ax
 80486e8:	66 90                	xchg   %ax,%ax
 80486ea:	66 90                	xchg   %ax,%ax
 80486ec:	66 90                	xchg   %ax,%ax
 80486ee:	66 90                	xchg   %ax,%ax

080486f0 <deregister_tm_clones>:
 80486f0:	b8 80 c2 04 08       	mov    $0x804c280,%eax
 80486f5:	3d 80 c2 04 08       	cmp    $0x804c280,%eax
 80486fa:	74 24                	je     8048720 <deregister_tm_clones+0x30>
 80486fc:	b8 00 00 00 00       	mov    $0x0,%eax
 8048701:	85 c0                	test   %eax,%eax
 8048703:	74 1b                	je     8048720 <deregister_tm_clones+0x30>
 8048705:	55                   	push   %ebp
 8048706:	89 e5                	mov    %esp,%ebp
 8048708:	83 ec 14             	sub    $0x14,%esp
 804870b:	68 80 c2 04 08       	push   $0x804c280
 8048710:	ff d0                	call   *%eax
 8048712:	83 c4 10             	add    $0x10,%esp
 8048715:	c9                   	leave
 8048716:	c3                   	ret
 8048717:	89 f6                	mov    %esi,%esi
 8048719:	8d bc 27 00 00 00 00 	lea    0x0(%edi,%eiz,1),%edi
 8048720:	f3 c3                	repz ret
 8048722:	8d b4 26 00 00 00 00 	lea    0x0(%esi,%eiz,1),%esi
 8048729:	8d bc 27 00 00 00 00 	lea    0x0(%edi,%eiz,1),%edi

08048730 <register_tm_clones>:
 8048730:	b8 80 c2 04 08       	mov    $0x804c280,%eax
 8048735:	2d 80 c2 04 08       	sub    $0x804c280,%eax
 804873a:	c1 f8 02             	sar    $0x2,%eax
 804873d:	89 c2                	mov    %eax,%edx
 804873f:	c1 ea 1f             	shr    $0x1f,%edx
 8048742:	01 d0                	add    %edx,%eax
 8048744:	d1 f8                	sar    $1,%eax
 8048746:	74 20                	je     8048768 <register_tm_clones+0x38>
 8048748:	ba 00 00 00 00       	mov    $0x0,%edx
 804874d:	85 d2                	test   %edx,%edx
 804874f:	74 17                	je     8048768 <register_tm_clones+0x38>
 8048751:	55                   	push   %ebp
 8048752:	89 e5                	mov    %esp,%ebp
 8048754:	83 ec 10             	sub    $0x10,%esp
 8048757:	50                   	push   %eax
 8048758:	68 80 c2 04 08       	push   $0x804c280
 804875d:	ff d2                	call   *%edx
 804875f:	83 c4 10             	add    $0x10,%esp
 8048762:	c9                   	leave
 8048763:	c3                   	ret
 8048764:	8d 74 26 00          	lea    0x0(%esi,%eiz,1),%esi
 8048768:	f3 c3                	repz ret
 804876a:	8d b6 00 00 00 00    	lea    0x0(%esi),%esi

08048770 <__do_global_dtors_aux>:
 8048770:	80 3d 88 c2 04 08 00 	cmpb   $0x0,0x804c288
 8048777:	75 17                	jne    8048790 <__do_global_dtors_aux+0x20>
 8048779:	55                   	push   %ebp
 804877a:	89 e5                	mov    %esp,%ebp
 804877c:	83 ec 08             	sub    $0x8,%esp
 804877f:	e8 6c ff ff ff       	call   80486f0 <deregister_tm_clones>
 8048784:	c6 05 88 c2 04 08 01 	movb   $0x1,0x804c288
 804878b:	c9                   	leave
 804878c:	c3                   	ret
 804878d:	8d 76 00             	lea    0x0(%esi),%esi
 8048790:	f3 c3                	repz ret
 8048792:	8d b4 26 00 00 00 00 	lea    0x0(%esi,%eiz,1),%esi
 8048799:	8d bc 27 00 00 00 00 	lea    0x0(%edi,%eiz,1),%edi

080487a0 <frame_dummy>:
 80487a0:	55                   	push   %ebp
 80487a1:	89 e5                	mov    %esp,%ebp
 80487a3:	5d                   	pop    %ebp
 80487a4:	eb 8a                	jmp    8048730 <register_tm_clones>

080487a6 <main>:
 80487a6:	8d 4c 24 04          	lea    0x4(%esp),%ecx
 80487aa:	83 e4 f0             	and    $0xfffffff0,%esp
 80487ad:	ff 71 fc             	push   -0x4(%ecx)
 80487b0:	55                   	push   %ebp
 80487b1:	89 e5                	mov    %esp,%ebp
 80487b3:	53                   	push   %ebx
 80487b4:	51                   	push   %ecx
 80487b5:	83 ec 10             	sub    $0x10,%esp
 80487b8:	89 cb                	mov    %ecx,%ebx
 80487ba:	83 3b 01             	cmpl   $0x1,(%ebx)
 80487bd:	75 0c                	jne    80487cb <main+0x25>
 80487bf:	a1 80 c2 04 08       	mov    0x804c280,%eax
 80487c4:	a3 90 c2 04 08       	mov    %eax,0x804c290
 80487c9:	eb 75                	jmp    8048840 <main+0x9a>
 80487cb:	83 3b 02             	cmpl   $0x2,(%ebx)
 80487ce:	75 50                	jne    8048820 <main+0x7a>
 80487d0:	8b 43 04             	mov    0x4(%ebx),%eax
 80487d3:	83 c0 04             	add    $0x4,%eax
 80487d6:	8b 00                	mov    (%eax),%eax
 80487d8:	83 ec 08             	sub    $0x8,%esp
 80487db:	68 68 96 04 08       	push   $0x8049668
 80487e0:	50                   	push   %eax
 80487e1:	e8 5a fe ff ff       	call   8048640 <fopen@plt>
 80487e6:	83 c4 10             	add    $0x10,%esp
 80487e9:	a3 90 c2 04 08       	mov    %eax,0x804c290
 80487ee:	a1 90 c2 04 08       	mov    0x804c290,%eax
 80487f3:	85 c0                	test   %eax,%eax
 80487f5:	75 49                	jne    8048840 <main+0x9a>
 80487f7:	8b 43 04             	mov    0x4(%ebx),%eax
 80487fa:	83 c0 04             	add    $0x4,%eax
 80487fd:	8b 10                	mov    (%eax),%edx
 80487ff:	8b 43 04             	mov    0x4(%ebx),%eax
 8048802:	8b 00                	mov    (%eax),%eax
 8048804:	83 ec 04             	sub    $0x4,%esp
 8048807:	52                   	push   %edx
 8048808:	50                   	push   %eax
 8048809:	68 6a 96 04 08       	push   $0x804966a
 804880e:	e8 6d fd ff ff       	call   8048580 <printf@plt>
 8048813:	83 c4 10             	add    $0x10,%esp
 8048816:	83 ec 0c             	sub    $0xc,%esp
 8048819:	6a 08                	push   $0x8
 804881b:	e8 e0 fd ff ff       	call   8048600 <exit@plt>
 8048820:	8b 43 04             	mov    0x4(%ebx),%eax
 8048823:	8b 00                	mov    (%eax),%eax
 8048825:	83 ec 08             	sub    $0x8,%esp
 8048828:	50                   	push   %eax
 8048829:	68 87 96 04 08       	push   $0x8049687
 804882e:	e8 4d fd ff ff       	call   8048580 <printf@plt>
 8048833:	83 c4 10             	add    $0x10,%esp
 8048836:	83 ec 0c             	sub    $0xc,%esp
 8048839:	6a 08                	push   $0x8
 804883b:	e8 c0 fd ff ff       	call   8048600 <exit@plt>
 8048840:	e8 b6 0a 00 00       	call   80492fb <initialize_bomb>
 8048845:	83 ec 0c             	sub    $0xc,%esp
 8048848:	68 a4 96 04 08       	push   $0x80496a4
 804884d:	e8 9e fd ff ff       	call   80485f0 <puts@plt>
 8048852:	83 c4 10             	add    $0x10,%esp
 8048855:	83 ec 0c             	sub    $0xc,%esp
 8048858:	68 e0 96 04 08       	push   $0x80496e0
 804885d:	e8 8e fd ff ff       	call   80485f0 <puts@plt>
 8048862:	83 c4 10             	add    $0x10,%esp
 8048865:	e8 4b 0b 00 00       	call   80493b5 <read_line>
 804886a:	89 45 f4             	mov    %eax,-0xc(%ebp)
 804886d:	83 ec 0c             	sub    $0xc,%esp
 8048870:	ff 75 f4             	push   -0xc(%ebp)
 8048873:	e8 57 01 00 00       	call   80489cf <phase_0>
 8048878:	83 c4 10             	add    $0x10,%esp
 804887b:	85 c0                	test   %eax,%eax
 804887d:	74 15                	je     8048894 <main+0xee>
 804887f:	e8 9d 0c 00 00       	call   8049521 <phase_defused>
 8048884:	83 ec 0c             	sub    $0xc,%esp
 8048887:	68 0c 97 04 08       	push   $0x804970c
 804888c:	e8 5f fd ff ff       	call   80485f0 <puts@plt>
 8048891:	83 c4 10             	add    $0x10,%esp
 8048894:	e8 1c 0b 00 00       	call   80493b5 <read_line>
 8048899:	89 45 f4             	mov    %eax,-0xc(%ebp)
 804889c:	83 ec 0c             	sub    $0xc,%esp
 804889f:	ff 75 f4             	push   -0xc(%ebp)
 80488a2:	e8 58 01 00 00       	call   80489ff <phase_1>
 80488a7:	83 c4 10             	add    $0x10,%esp
 80488aa:	85 c0                	test   %eax,%eax
 80488ac:	74 15                	je     80488c3 <main+0x11d>
 80488ae:	e8 6e 0c 00 00       	call   8049521 <phase_defused>
 80488b3:	83 ec 0c             	sub    $0xc,%esp
 80488b6:	68 34 97 04 08       	push   $0x8049734
 80488bb:	e8 30 fd ff ff       	call   80485f0 <puts@plt>
 80488c0:	83 c4 10             	add    $0x10,%esp
 80488c3:	e8 ed 0a 00 00       	call   80493b5 <read_line>
 80488c8:	89 45 f4             	mov    %eax,-0xc(%ebp)
 80488cb:	83 ec 0c             	sub    $0xc,%esp
 80488ce:	ff 75 f4             	push   -0xc(%ebp)
 80488d1:	e8 bd 01 00 00       	call   8048a93 <phase_2>
 80488d6:	83 c4 10             	add    $0x10,%esp
 80488d9:	85 c0                	test   %eax,%eax
 80488db:	74 15                	je     80488f2 <main+0x14c>
 80488dd:	e8 3f 0c 00 00       	call   8049521 <phase_defused>
 80488e2:	83 ec 0c             	sub    $0xc,%esp
 80488e5:	68 5d 97 04 08       	push   $0x804975d
 80488ea:	e8 01 fd ff ff       	call   80485f0 <puts@plt>
 80488ef:	83 c4 10             	add    $0x10,%esp
 80488f2:	e8 be 0a 00 00       	call   80493b5 <read_line>
 80488f7:	89 45 f4             	mov    %eax,-0xc(%ebp)
 80488fa:	83 ec 0c             	sub    $0xc,%esp
 80488fd:	ff 75 f4             	push   -0xc(%ebp)
 8048900:	e8 2b 02 00 00       	call   8048b30 <phase_3>
 8048905:	83 c4 10             	add    $0x10,%esp
 8048908:	85 c0                	test   %eax,%eax
 804890a:	74 15                	je     8048921 <main+0x17b>
 804890c:	e8 10 0c 00 00       	call   8049521 <phase_defused>
 8048911:	83 ec 0c             	sub    $0xc,%esp
 8048914:	68 7b 97 04 08       	push   $0x804977b
 8048919:	e8 d2 fc ff ff       	call   80485f0 <puts@plt>
 804891e:	83 c4 10             	add    $0x10,%esp
 8048921:	e8 8f 0a 00 00       	call   80493b5 <read_line>
 8048926:	89 45 f4             	mov    %eax,-0xc(%ebp)
 8048929:	83 ec 0c             	sub    $0xc,%esp
 804892c:	ff 75 f4             	push   -0xc(%ebp)
 804892f:	e8 00 04 00 00       	call   8048d34 <phase_4>
 8048934:	83 c4 10             	add    $0x10,%esp
 8048937:	85 c0                	test   %eax,%eax
 8048939:	74 15                	je     8048950 <main+0x1aa>
 804893b:	e8 e1 0b 00 00       	call   8049521 <phase_defused>
 8048940:	83 ec 0c             	sub    $0xc,%esp
 8048943:	68 8c 97 04 08       	push   $0x804978c
 8048948:	e8 a3 fc ff ff       	call   80485f0 <puts@plt>
 804894d:	83 c4 10             	add    $0x10,%esp
 8048950:	e8 60 0a 00 00       	call   80493b5 <read_line>
 8048955:	89 45 f4             	mov    %eax,-0xc(%ebp)
 8048958:	83 ec 0c             	sub    $0xc,%esp
 804895b:	ff 75 f4             	push   -0xc(%ebp)
 804895e:	e8 6d 04 00 00       	call   8048dd0 <phase_5>
 8048963:	83 c4 10             	add    $0x10,%esp
 8048966:	85 c0                	test   %eax,%eax
 8048968:	74 15                	je     804897f <main+0x1d9>
 804896a:	e8 b2 0b 00 00       	call   8049521 <phase_defused>
 804896f:	83 ec 0c             	sub    $0xc,%esp
 8048972:	68 b0 97 04 08       	push   $0x80497b0
 8048977:	e8 74 fc ff ff       	call   80485f0 <puts@plt>
 804897c:	83 c4 10             	add    $0x10,%esp
 804897f:	e8 31 0a 00 00       	call   80493b5 <read_line>
 8048984:	89 45 f4             	mov    %eax,-0xc(%ebp)
 8048987:	83 ec 0c             	sub    $0xc,%esp
 804898a:	ff 75 f4             	push   -0xc(%ebp)
 804898d:	e8 ec 04 00 00       	call   8048e7e <phase_6>
 8048992:	83 c4 10             	add    $0x10,%esp
 8048995:	85 c0                	test   %eax,%eax
 8048997:	74 05                	je     804899e <main+0x1f8>
 8048999:	e8 83 0b 00 00       	call   8049521 <phase_defused>
 804899e:	b8 00 00 00 00       	mov    $0x0,%eax
 80489a3:	8d 65 f8             	lea    -0x8(%ebp),%esp
 80489a6:	59                   	pop    %ecx
 80489a7:	5b                   	pop    %ebx
 80489a8:	5d                   	pop    %ebp
 80489a9:	8d 61 fc             	lea    -0x4(%ecx),%esp
 80489ac:	c3                   	ret

080489ad <FYGkyfYK>:
 80489ad:	55                   	push   %ebp
 80489ae:	89 e5                	mov    %esp,%ebp
 80489b0:	53                   	push   %ebx
 80489b1:	8b 45 0c             	mov    0xc(%ebp),%eax
 80489b4:	8b 55 08             	mov    0x8(%ebp),%edx
 80489b7:	89 d3                	mov    %edx,%ebx
 80489b9:	89 c1                	mov    %eax,%ecx
 80489bb:	d3 fb                	sar    %cl,%ebx
 80489bd:	8b 45 08             	mov    0x8(%ebp),%eax
 80489c0:	8b 55 0c             	mov    0xc(%ebp),%edx
 80489c3:	89 c1                	mov    %eax,%ecx
 80489c5:	d3 e2                	shl    %cl,%edx
 80489c7:	89 d0                	mov    %edx,%eax
 80489c9:	0f af c3             	imul   %ebx,%eax
 80489cc:	5b                   	pop    %ebx
 80489cd:	5d                   	pop    %ebp
 80489ce:	c3                   	ret

080489cf <phase_0>:
 80489cf:	55                   	push   %ebp
 80489d0:	89 e5                	mov    %esp,%ebp
 80489d2:	83 ec 08             	sub    $0x8,%esp
 80489d5:	83 ec 08             	sub    $0x8,%esp
 80489d8:	68 28 98 04 08       	push   $0x8049828
 80489dd:	ff 75 08             	push   0x8(%ebp)
 80489e0:	e8 ab 08 00 00       	call   8049290 <strings_not_equal>
 80489e5:	83 c4 10             	add    $0x10,%esp
 80489e8:	85 c0                	test   %eax,%eax
 80489ea:	74 0c                	je     80489f8 <phase_0+0x29>
 80489ec:	e8 07 0b 00 00       	call   80494f8 <explode_bomb>
 80489f1:	b8 00 00 00 00       	mov    $0x0,%eax
 80489f6:	eb 05                	jmp    80489fd <phase_0+0x2e>
 80489f8:	b8 01 00 00 00       	mov    $0x1,%eax
 80489fd:	c9                   	leave
 80489fe:	c3                   	ret

080489ff <phase_1>:
 80489ff:	55                   	push   %ebp
 8048a00:	89 e5                	mov    %esp,%ebp
 8048a02:	83 ec 38             	sub    $0x38,%esp
 8048a05:	8b 45 08             	mov    0x8(%ebp),%eax
 8048a08:	89 45 d4             	mov    %eax,-0x2c(%ebp)
 8048a0b:	65 a1 14 00 00 00    	mov    %gs:0x14,%eax
 8048a11:	89 45 f4             	mov    %eax,-0xc(%ebp)
 8048a14:	31 c0                	xor    %eax,%eax
 8048a16:	c7 45 f0 d7 45 13 1b 	movl   $0x1b1345d7,-0x10(%ebp)
 8048a1d:	db 45 f0             	fildl  -0x10(%ebp)
 8048a20:	d9 5d e4             	fstps  -0x1c(%ebp)
 8048a23:	8d 45 ec             	lea    -0x14(%ebp),%eax
 8048a26:	50                   	push   %eax
 8048a27:	8d 45 e8             	lea    -0x18(%ebp),%eax
 8048a2a:	50                   	push   %eax
 8048a2b:	68 56 98 04 08       	push   $0x8049856
 8048a30:	ff 75 d4             	push   -0x2c(%ebp)
 8048a33:	e8 f8 fb ff ff       	call   8048630 <__isoc99_sscanf@plt>
 8048a38:	83 c4 10             	add    $0x10,%esp
 8048a3b:	83 f8 02             	cmp    $0x2,%eax
 8048a3e:	74 0c                	je     8048a4c <phase_1+0x4d>
 8048a40:	e8 b3 0a 00 00       	call   80494f8 <explode_bomb>
 8048a45:	b8 00 00 00 00       	mov    $0x0,%eax
 8048a4a:	eb 34                	jmp    8048a80 <phase_1+0x81>
 8048a4c:	8d 45 e4             	lea    -0x1c(%ebp),%eax
 8048a4f:	83 c0 02             	add    $0x2,%eax
 8048a52:	0f b7 00             	movzwl (%eax),%eax
 8048a55:	0f bf d0             	movswl %ax,%edx
 8048a58:	8b 45 e8             	mov    -0x18(%ebp),%eax
 8048a5b:	39 c2                	cmp    %eax,%edx
 8048a5d:	75 10                	jne    8048a6f <phase_1+0x70>
 8048a5f:	8d 45 e4             	lea    -0x1c(%ebp),%eax
 8048a62:	0f b7 00             	movzwl (%eax),%eax
 8048a65:	0f bf d0             	movswl %ax,%edx
 8048a68:	8b 45 ec             	mov    -0x14(%ebp),%eax
 8048a6b:	39 c2                	cmp    %eax,%edx
 8048a6d:	74 0c                	je     8048a7b <phase_1+0x7c>
 8048a6f:	e8 84 0a 00 00       	call   80494f8 <explode_bomb>
 8048a74:	b8 00 00 00 00       	mov    $0x0,%eax
 8048a79:	eb 05                	jmp    8048a80 <phase_1+0x81>
 8048a7b:	b8 01 00 00 00       	mov    $0x1,%eax
 8048a80:	8b 4d f4             	mov    -0xc(%ebp),%ecx
 8048a83:	65 33 0d 14 00 00 00 	xor    %gs:0x14,%ecx
 8048a8a:	74 05                	je     8048a91 <phase_1+0x92>
 8048a8c:	e8 3f fb ff ff       	call   80485d0 <__stack_chk_fail@plt>
 8048a91:	c9                   	leave
 8048a92:	c3                   	ret

08048a93 <phase_2>:
 8048a93:	55                   	push   %ebp
 8048a94:	89 e5                	mov    %esp,%ebp
 8048a96:	83 ec 48             	sub    $0x48,%esp
 8048a99:	8b 45 08             	mov    0x8(%ebp),%eax
 8048a9c:	89 45 c4             	mov    %eax,-0x3c(%ebp)
 8048a9f:	65 a1 14 00 00 00    	mov    %gs:0x14,%eax
 8048aa5:	89 45 f4             	mov    %eax,-0xc(%ebp)
 8048aa8:	31 c0                	xor    %eax,%eax
 8048aaa:	83 ec 04             	sub    $0x4,%esp
 8048aad:	6a 08                	push   $0x8
 8048aaf:	8d 45 d4             	lea    -0x2c(%ebp),%eax
 8048ab2:	50                   	push   %eax
 8048ab3:	ff 75 c4             	push   -0x3c(%ebp)
 8048ab6:	e8 1b 07 00 00       	call   80491d6 <read_n_numbers>
 8048abb:	83 c4 10             	add    $0x10,%esp
 8048abe:	85 c0                	test   %eax,%eax
 8048ac0:	75 07                	jne    8048ac9 <phase_2+0x36>
 8048ac2:	b8 00 00 00 00       	mov    $0x0,%eax
 8048ac7:	eb 54                	jmp    8048b1d <phase_2+0x8a>
 8048ac9:	8b 45 d4             	mov    -0x2c(%ebp),%eax
 8048acc:	3d e0 00 00 00       	cmp    $0xe0,%eax
 8048ad1:	74 0c                	je     8048adf <phase_2+0x4c>
 8048ad3:	e8 20 0a 00 00       	call   80494f8 <explode_bomb>
 8048ad8:	b8 00 00 00 00       	mov    $0x0,%eax
 8048add:	eb 3e                	jmp    8048b1d <phase_2+0x8a>
 8048adf:	c7 45 d0 01 00 00 00 	movl   $0x1,-0x30(%ebp)
 8048ae6:	eb 2a                	jmp    8048b12 <phase_2+0x7f>
 8048ae8:	8b 45 d0             	mov    -0x30(%ebp),%eax
 8048aeb:	8b 44 85 d4          	mov    -0x2c(%ebp,%eax,4),%eax
 8048aef:	8b 55 d0             	mov    -0x30(%ebp),%edx
 8048af2:	83 ea 01             	sub    $0x1,%edx
 8048af5:	8b 54 95 d4          	mov    -0x2c(%ebp,%edx,4),%edx
 8048af9:	d1 fa                	sar    $1,%edx
 8048afb:	83 c2 01             	add    $0x1,%edx
 8048afe:	39 d0                	cmp    %edx,%eax
 8048b00:	74 0c                	je     8048b0e <phase_2+0x7b>
 8048b02:	e8 f1 09 00 00       	call   80494f8 <explode_bomb>
 8048b07:	b8 00 00 00 00       	mov    $0x0,%eax
 8048b0c:	eb 0f                	jmp    8048b1d <phase_2+0x8a>
 8048b0e:	83 45 d0 01          	addl   $0x1,-0x30(%ebp)
 8048b12:	83 7d d0 07          	cmpl   $0x7,-0x30(%ebp)
 8048b16:	7e d0                	jle    8048ae8 <phase_2+0x55>
 8048b18:	b8 01 00 00 00       	mov    $0x1,%eax
 8048b1d:	8b 4d f4             	mov    -0xc(%ebp),%ecx
 8048b20:	65 33 0d 14 00 00 00 	xor    %gs:0x14,%ecx
 8048b27:	74 05                	je     8048b2e <phase_2+0x9b>
 8048b29:	e8 a2 fa ff ff       	call   80485d0 <__stack_chk_fail@plt>
 8048b2e:	c9                   	leave
 8048b2f:	c3                   	ret

08048b30 <phase_3>:
 8048b30:	55                   	push   %ebp
 8048b31:	89 e5                	mov    %esp,%ebp
 8048b33:	83 ec 38             	sub    $0x38,%esp
 8048b36:	8b 45 08             	mov    0x8(%ebp),%eax
 8048b39:	89 45 d4             	mov    %eax,-0x2c(%ebp)
 8048b3c:	65 a1 14 00 00 00    	mov    %gs:0x14,%eax
 8048b42:	89 45 f4             	mov    %eax,-0xc(%ebp)
 8048b45:	31 c0                	xor    %eax,%eax
 8048b47:	c7 45 f0 00 00 00 00 	movl   $0x0,-0x10(%ebp)
 8048b4e:	83 ec 0c             	sub    $0xc,%esp
 8048b51:	8d 45 ec             	lea    -0x14(%ebp),%eax
 8048b54:	50                   	push   %eax
 8048b55:	8d 45 e6             	lea    -0x1a(%ebp),%eax
 8048b58:	50                   	push   %eax
 8048b59:	8d 45 e8             	lea    -0x18(%ebp),%eax
 8048b5c:	50                   	push   %eax
 8048b5d:	68 5c 98 04 08       	push   $0x804985c
 8048b62:	ff 75 d4             	push   -0x2c(%ebp)
 8048b65:	e8 c6 fa ff ff       	call   8048630 <__isoc99_sscanf@plt>
 8048b6a:	83 c4 20             	add    $0x20,%esp
 8048b6d:	89 45 f0             	mov    %eax,-0x10(%ebp)
 8048b70:	83 7d f0 02          	cmpl   $0x2,-0x10(%ebp)
 8048b74:	7f 0f                	jg     8048b85 <phase_3+0x55>
 8048b76:	e8 7d 09 00 00       	call   80494f8 <explode_bomb>
 8048b7b:	b8 00 00 00 00       	mov    $0x0,%eax
 8048b80:	e9 44 01 00 00       	jmp    8048cc9 <phase_3+0x199>
 8048b85:	8b 45 e8             	mov    -0x18(%ebp),%eax
 8048b88:	83 f8 07             	cmp    $0x7,%eax
 8048b8b:	0f 87 f8 00 00 00    	ja     8048c89 <phase_3+0x159>
 8048b91:	8b 04 85 68 98 04 08 	mov    0x8049868(,%eax,4),%eax
 8048b98:	ff e0                	jmp    *%eax
 8048b9a:	c6 45 e7 73          	movb   $0x73,-0x19(%ebp)
 8048b9e:	8b 45 ec             	mov    -0x14(%ebp),%eax
 8048ba1:	3d a5 01 00 00       	cmp    $0x1a5,%eax
 8048ba6:	0f 84 ed 00 00 00    	je     8048c99 <phase_3+0x169>
 8048bac:	e8 47 09 00 00       	call   80494f8 <explode_bomb>
 8048bb1:	b8 00 00 00 00       	mov    $0x0,%eax
 8048bb6:	e9 0e 01 00 00       	jmp    8048cc9 <phase_3+0x199>
 8048bbb:	c6 45 e7 73          	movb   $0x73,-0x19(%ebp)
 8048bbf:	8b 45 ec             	mov    -0x14(%ebp),%eax
 8048bc2:	3d a5 01 00 00       	cmp    $0x1a5,%eax
 8048bc7:	0f 84 cf 00 00 00    	je     8048c9c <phase_3+0x16c>
 8048bcd:	e8 26 09 00 00       	call   80494f8 <explode_bomb>
 8048bd2:	b8 00 00 00 00       	mov    $0x0,%eax
 8048bd7:	e9 ed 00 00 00       	jmp    8048cc9 <phase_3+0x199>
 8048bdc:	c6 45 e7 73          	movb   $0x73,-0x19(%ebp)
 8048be0:	8b 45 ec             	mov    -0x14(%ebp),%eax
 8048be3:	3d a5 01 00 00       	cmp    $0x1a5,%eax
 8048be8:	0f 84 b1 00 00 00    	je     8048c9f <phase_3+0x16f>
 8048bee:	e8 05 09 00 00       	call   80494f8 <explode_bomb>
 8048bf3:	b8 00 00 00 00       	mov    $0x0,%eax
 8048bf8:	e9 cc 00 00 00       	jmp    8048cc9 <phase_3+0x199>
 8048bfd:	c6 45 e7 73          	movb   $0x73,-0x19(%ebp)
 8048c01:	8b 45 ec             	mov    -0x14(%ebp),%eax
 8048c04:	3d a5 01 00 00       	cmp    $0x1a5,%eax
 8048c09:	0f 84 93 00 00 00    	je     8048ca2 <phase_3+0x172>
 8048c0f:	e8 e4 08 00 00       	call   80494f8 <explode_bomb>
 8048c14:	b8 00 00 00 00       	mov    $0x0,%eax
 8048c19:	e9 ab 00 00 00       	jmp    8048cc9 <phase_3+0x199>
 8048c1e:	c6 45 e7 73          	movb   $0x73,-0x19(%ebp)
 8048c22:	8b 45 ec             	mov    -0x14(%ebp),%eax
 8048c25:	3d a5 01 00 00       	cmp    $0x1a5,%eax
 8048c2a:	74 79                	je     8048ca5 <phase_3+0x175>
 8048c2c:	e8 c7 08 00 00       	call   80494f8 <explode_bomb>
 8048c31:	b8 00 00 00 00       	mov    $0x0,%eax
 8048c36:	e9 8e 00 00 00       	jmp    8048cc9 <phase_3+0x199>
 8048c3b:	c6 45 e7 61          	movb   $0x61,-0x19(%ebp)
 8048c3f:	8b 45 ec             	mov    -0x14(%ebp),%eax
 8048c42:	3d b1 00 00 00       	cmp    $0xb1,%eax
 8048c47:	74 5f                	je     8048ca8 <phase_3+0x178>
 8048c49:	e8 aa 08 00 00       	call   80494f8 <explode_bomb>
 8048c4e:	b8 00 00 00 00       	mov    $0x0,%eax
 8048c53:	eb 74                	jmp    8048cc9 <phase_3+0x199>
 8048c55:	c6 45 e7 73          	movb   $0x73,-0x19(%ebp)
 8048c59:	8b 45 ec             	mov    -0x14(%ebp),%eax
 8048c5c:	3d a5 01 00 00       	cmp    $0x1a5,%eax
 8048c61:	74 48                	je     8048cab <phase_3+0x17b>
 8048c63:	e8 90 08 00 00       	call   80494f8 <explode_bomb>
 8048c68:	b8 00 00 00 00       	mov    $0x0,%eax
 8048c6d:	eb 5a                	jmp    8048cc9 <phase_3+0x199>
 8048c6f:	c6 45 e7 73          	movb   $0x73,-0x19(%ebp)
 8048c73:	8b 45 ec             	mov    -0x14(%ebp),%eax
 8048c76:	3d a5 01 00 00       	cmp    $0x1a5,%eax
 8048c7b:	74 31                	je     8048cae <phase_3+0x17e>
 8048c7d:	e8 76 08 00 00       	call   80494f8 <explode_bomb>
 8048c82:	b8 00 00 00 00       	mov    $0x0,%eax
 8048c87:	eb 40                	jmp    8048cc9 <phase_3+0x199>
 8048c89:	c6 45 e7 73          	movb   $0x73,-0x19(%ebp)
 8048c8d:	e8 66 08 00 00       	call   80494f8 <explode_bomb>
 8048c92:	b8 00 00 00 00       	mov    $0x0,%eax
 8048c97:	eb 30                	jmp    8048cc9 <phase_3+0x199>
 8048c99:	90                   	nop
 8048c9a:	eb 13                	jmp    8048caf <phase_3+0x17f>
 8048c9c:	90                   	nop
 8048c9d:	eb 10                	jmp    8048caf <phase_3+0x17f>
 8048c9f:	90                   	nop
 8048ca0:	eb 0d                	jmp    8048caf <phase_3+0x17f>
 8048ca2:	90                   	nop
 8048ca3:	eb 0a                	jmp    8048caf <phase_3+0x17f>
 8048ca5:	90                   	nop
 8048ca6:	eb 07                	jmp    8048caf <phase_3+0x17f>
 8048ca8:	90                   	nop
 8048ca9:	eb 04                	jmp    8048caf <phase_3+0x17f>
 8048cab:	90                   	nop
 8048cac:	eb 01                	jmp    8048caf <phase_3+0x17f>
 8048cae:	90                   	nop
 8048caf:	0f b6 45 e6          	movzbl -0x1a(%ebp),%eax
 8048cb3:	38 45 e7             	cmp    %al,-0x19(%ebp)
 8048cb6:	74 0c                	je     8048cc4 <phase_3+0x194>
 8048cb8:	e8 3b 08 00 00       	call   80494f8 <explode_bomb>
 8048cbd:	b8 00 00 00 00       	mov    $0x0,%eax
 8048cc2:	eb 05                	jmp    8048cc9 <phase_3+0x199>
 8048cc4:	b8 01 00 00 00       	mov    $0x1,%eax
 8048cc9:	8b 55 f4             	mov    -0xc(%ebp),%edx
 8048ccc:	65 33 15 14 00 00 00 	xor    %gs:0x14,%edx
 8048cd3:	74 05                	je     8048cda <phase_3+0x1aa>
 8048cd5:	e8 f6 f8 ff ff       	call   80485d0 <__stack_chk_fail@plt>
 8048cda:	c9                   	leave
 8048cdb:	c3                   	ret

08048cdc <func4>:
 8048cdc:	55                   	push   %ebp
 8048cdd:	89 e5                	mov    %esp,%ebp
 8048cdf:	53                   	push   %ebx
 8048ce0:	83 ec 04             	sub    $0x4,%esp
 8048ce3:	83 7d 08 00          	cmpl   $0x0,0x8(%ebp)
 8048ce7:	7f 07                	jg     8048cf0 <func4+0x14>
 8048ce9:	b8 00 00 00 00       	mov    $0x0,%eax
 8048cee:	eb 3f                	jmp    8048d2f <func4+0x53>
 8048cf0:	83 7d 08 01          	cmpl   $0x1,0x8(%ebp)
 8048cf4:	75 05                	jne    8048cfb <func4+0x1f>
 8048cf6:	8b 45 0c             	mov    0xc(%ebp),%eax
 8048cf9:	eb 34                	jmp    8048d2f <func4+0x53>
 8048cfb:	8b 45 08             	mov    0x8(%ebp),%eax
 8048cfe:	83 e8 01             	sub    $0x1,%eax
 8048d01:	83 ec 08             	sub    $0x8,%esp
 8048d04:	ff 75 0c             	push   0xc(%ebp)
 8048d07:	50                   	push   %eax
 8048d08:	e8 cf ff ff ff       	call   8048cdc <func4>
 8048d0d:	83 c4 10             	add    $0x10,%esp
 8048d10:	89 c2                	mov    %eax,%edx
 8048d12:	8b 45 0c             	mov    0xc(%ebp),%eax
 8048d15:	8d 1c 02             	lea    (%edx,%eax,1),%ebx
 8048d18:	8b 45 08             	mov    0x8(%ebp),%eax
 8048d1b:	83 e8 02             	sub    $0x2,%eax
 8048d1e:	83 ec 08             	sub    $0x8,%esp
 8048d21:	ff 75 0c             	push   0xc(%ebp)
 8048d24:	50                   	push   %eax
 8048d25:	e8 b2 ff ff ff       	call   8048cdc <func4>
 8048d2a:	83 c4 10             	add    $0x10,%esp
 8048d2d:	01 d8                	add    %ebx,%eax
 8048d2f:	8b 5d fc             	mov    -0x4(%ebp),%ebx
 8048d32:	c9                   	leave
 8048d33:	c3                   	ret

08048d34 <phase_4>:
 8048d34:	55                   	push   %ebp
 8048d35:	89 e5                	mov    %esp,%ebp
 8048d37:	83 ec 38             	sub    $0x38,%esp
 8048d3a:	8b 45 08             	mov    0x8(%ebp),%eax
 8048d3d:	89 45 d4             	mov    %eax,-0x2c(%ebp)
 8048d40:	65 a1 14 00 00 00    	mov    %gs:0x14,%eax
 8048d46:	89 45 f4             	mov    %eax,-0xc(%ebp)
 8048d49:	31 c0                	xor    %eax,%eax
 8048d4b:	8d 45 e0             	lea    -0x20(%ebp),%eax
 8048d4e:	50                   	push   %eax
 8048d4f:	8d 45 e4             	lea    -0x1c(%ebp),%eax
 8048d52:	50                   	push   %eax
 8048d53:	68 56 98 04 08       	push   $0x8049856
 8048d58:	ff 75 d4             	push   -0x2c(%ebp)
 8048d5b:	e8 d0 f8 ff ff       	call   8048630 <__isoc99_sscanf@plt>
 8048d60:	83 c4 10             	add    $0x10,%esp
 8048d63:	89 45 e8             	mov    %eax,-0x18(%ebp)
 8048d66:	83 7d e8 02          	cmpl   $0x2,-0x18(%ebp)
 8048d6a:	75 10                	jne    8048d7c <phase_4+0x48>
 8048d6c:	8b 45 e0             	mov    -0x20(%ebp),%eax
 8048d6f:	83 f8 01             	cmp    $0x1,%eax
 8048d72:	7e 08                	jle    8048d7c <phase_4+0x48>
 8048d74:	8b 45 e0             	mov    -0x20(%ebp),%eax
 8048d77:	83 f8 04             	cmp    $0x4,%eax
 8048d7a:	7e 0c                	jle    8048d88 <phase_4+0x54>
 8048d7c:	e8 77 07 00 00       	call   80494f8 <explode_bomb>
 8048d81:	b8 00 00 00 00       	mov    $0x0,%eax
 8048d86:	eb 35                	jmp    8048dbd <phase_4+0x89>
 8048d88:	c7 45 ec 07 00 00 00 	movl   $0x7,-0x14(%ebp)
 8048d8f:	8b 45 e0             	mov    -0x20(%ebp),%eax
 8048d92:	83 ec 08             	sub    $0x8,%esp
 8048d95:	50                   	push   %eax
 8048d96:	ff 75 ec             	push   -0x14(%ebp)
 8048d99:	e8 3e ff ff ff       	call   8048cdc <func4>
 8048d9e:	83 c4 10             	add    $0x10,%esp
 8048da1:	89 45 f0             	mov    %eax,-0x10(%ebp)
 8048da4:	8b 45 e4             	mov    -0x1c(%ebp),%eax
 8048da7:	39 45 f0             	cmp    %eax,-0x10(%ebp)
 8048daa:	74 0c                	je     8048db8 <phase_4+0x84>
 8048dac:	e8 47 07 00 00       	call   80494f8 <explode_bomb>
 8048db1:	b8 00 00 00 00       	mov    $0x0,%eax
 8048db6:	eb 05                	jmp    8048dbd <phase_4+0x89>
 8048db8:	b8 01 00 00 00       	mov    $0x1,%eax
 8048dbd:	8b 55 f4             	mov    -0xc(%ebp),%edx
 8048dc0:	65 33 15 14 00 00 00 	xor    %gs:0x14,%edx
 8048dc7:	74 05                	je     8048dce <phase_4+0x9a>
 8048dc9:	e8 02 f8 ff ff       	call   80485d0 <__stack_chk_fail@plt>
 8048dce:	c9                   	leave
 8048dcf:	c3                   	ret

08048dd0 <phase_5>:
 8048dd0:	55                   	push   %ebp
 8048dd1:	89 e5                	mov    %esp,%ebp
 8048dd3:	83 ec 38             	sub    $0x38,%esp
 8048dd6:	8b 45 08             	mov    0x8(%ebp),%eax
 8048dd9:	89 45 d4             	mov    %eax,-0x2c(%ebp)
 8048ddc:	65 a1 14 00 00 00    	mov    %gs:0x14,%eax
 8048de2:	89 45 f4             	mov    %eax,-0xc(%ebp)
 8048de5:	31 c0                	xor    %eax,%eax
 8048de7:	8d 45 e4             	lea    -0x1c(%ebp),%eax
 8048dea:	50                   	push   %eax
 8048deb:	8d 45 e0             	lea    -0x20(%ebp),%eax
 8048dee:	50                   	push   %eax
 8048def:	68 56 98 04 08       	push   $0x8049856
 8048df4:	ff 75 d4             	push   -0x2c(%ebp)
 8048df7:	e8 34 f8 ff ff       	call   8048630 <__isoc99_sscanf@plt>
 8048dfc:	83 c4 10             	add    $0x10,%esp
 8048dff:	89 45 f0             	mov    %eax,-0x10(%ebp)
 8048e02:	83 7d f0 01          	cmpl   $0x1,-0x10(%ebp)
 8048e06:	7f 0c                	jg     8048e14 <phase_5+0x44>
 8048e08:	e8 eb 06 00 00       	call   80494f8 <explode_bomb>
 8048e0d:	b8 00 00 00 00       	mov    $0x0,%eax
 8048e12:	eb 57                	jmp    8048e6b <phase_5+0x9b>
 8048e14:	8b 45 e0             	mov    -0x20(%ebp),%eax
 8048e17:	83 e0 0f             	and    $0xf,%eax
 8048e1a:	89 45 e0             	mov    %eax,-0x20(%ebp)
 8048e1d:	c7 45 e8 00 00 00 00 	movl   $0x0,-0x18(%ebp)
 8048e24:	c7 45 ec 00 00 00 00 	movl   $0x0,-0x14(%ebp)
 8048e2b:	eb 17                	jmp    8048e44 <phase_5+0x74>
 8048e2d:	83 45 e8 01          	addl   $0x1,-0x18(%ebp)
 8048e31:	8b 45 e0             	mov    -0x20(%ebp),%eax
 8048e34:	8b 04 85 40 c2 04 08 	mov    0x804c240(,%eax,4),%eax
 8048e3b:	89 45 e0             	mov    %eax,-0x20(%ebp)
 8048e3e:	8b 45 e0             	mov    -0x20(%ebp),%eax
 8048e41:	01 45 ec             	add    %eax,-0x14(%ebp)
 8048e44:	8b 45 e0             	mov    -0x20(%ebp),%eax
 8048e47:	83 f8 0f             	cmp    $0xf,%eax
 8048e4a:	75 e1                	jne    8048e2d <phase_5+0x5d>
 8048e4c:	83 7d e8 08          	cmpl   $0x8,-0x18(%ebp)
 8048e50:	75 08                	jne    8048e5a <phase_5+0x8a>
 8048e52:	8b 45 e4             	mov    -0x1c(%ebp),%eax
 8048e55:	39 45 ec             	cmp    %eax,-0x14(%ebp)
 8048e58:	74 0c                	je     8048e66 <phase_5+0x96>
 8048e5a:	e8 99 06 00 00       	call   80494f8 <explode_bomb>
 8048e5f:	b8 00 00 00 00       	mov    $0x0,%eax
 8048e64:	eb 05                	jmp    8048e6b <phase_5+0x9b>
 8048e66:	b8 01 00 00 00       	mov    $0x1,%eax
 8048e6b:	8b 55 f4             	mov    -0xc(%ebp),%edx
 8048e6e:	65 33 15 14 00 00 00 	xor    %gs:0x14,%edx
 8048e75:	74 05                	je     8048e7c <phase_5+0xac>
 8048e77:	e8 54 f7 ff ff       	call   80485d0 <__stack_chk_fail@plt>
 8048e7c:	c9                   	leave
 8048e7d:	c3                   	ret

08048e7e <phase_6>:
 8048e7e:	55                   	push   %ebp
 8048e7f:	89 e5                	mov    %esp,%ebp
 8048e81:	83 ec 68             	sub    $0x68,%esp
 8048e84:	8b 45 08             	mov    0x8(%ebp),%eax
 8048e87:	89 45 a4             	mov    %eax,-0x5c(%ebp)
 8048e8a:	65 a1 14 00 00 00    	mov    %gs:0x14,%eax
 8048e90:	89 45 f4             	mov    %eax,-0xc(%ebp)
 8048e93:	31 c0                	xor    %eax,%eax
 8048e95:	c7 45 b8 80 c1 04 08 	movl   $0x804c180,-0x48(%ebp)
 8048e9c:	83 ec 04             	sub    $0x4,%esp
 8048e9f:	6a 07                	push   $0x7
 8048ea1:	8d 45 bc             	lea    -0x44(%ebp),%eax
 8048ea4:	50                   	push   %eax
 8048ea5:	ff 75 a4             	push   -0x5c(%ebp)
 8048ea8:	e8 29 03 00 00       	call   80491d6 <read_n_numbers>
 8048ead:	83 c4 10             	add    $0x10,%esp
 8048eb0:	85 c0                	test   %eax,%eax
 8048eb2:	75 0a                	jne    8048ebe <phase_6+0x40>
 8048eb4:	b8 00 00 00 00       	mov    $0x0,%eax
 8048eb9:	e9 37 01 00 00       	jmp    8048ff5 <phase_6+0x177>
 8048ebe:	c7 45 b0 00 00 00 00 	movl   $0x0,-0x50(%ebp)
 8048ec5:	eb 60                	jmp    8048f27 <phase_6+0xa9>
 8048ec7:	8b 45 b0             	mov    -0x50(%ebp),%eax
 8048eca:	8b 44 85 bc          	mov    -0x44(%ebp,%eax,4),%eax
 8048ece:	85 c0                	test   %eax,%eax
 8048ed0:	7e 0c                	jle    8048ede <phase_6+0x60>
 8048ed2:	8b 45 b0             	mov    -0x50(%ebp),%eax
 8048ed5:	8b 44 85 bc          	mov    -0x44(%ebp,%eax,4),%eax
 8048ed9:	83 f8 07             	cmp    $0x7,%eax
 8048edc:	7e 0f                	jle    8048eed <phase_6+0x6f>
 8048ede:	e8 15 06 00 00       	call   80494f8 <explode_bomb>
 8048ee3:	b8 00 00 00 00       	mov    $0x0,%eax
 8048ee8:	e9 08 01 00 00       	jmp    8048ff5 <phase_6+0x177>
 8048eed:	8b 45 b0             	mov    -0x50(%ebp),%eax
 8048ef0:	83 c0 01             	add    $0x1,%eax
 8048ef3:	89 45 b4             	mov    %eax,-0x4c(%ebp)
 8048ef6:	eb 25                	jmp    8048f1d <phase_6+0x9f>
 8048ef8:	8b 45 b0             	mov    -0x50(%ebp),%eax
 8048efb:	8b 54 85 bc          	mov    -0x44(%ebp,%eax,4),%edx
 8048eff:	8b 45 b4             	mov    -0x4c(%ebp),%eax
 8048f02:	8b 44 85 bc          	mov    -0x44(%ebp,%eax,4),%eax
 8048f06:	39 c2                	cmp    %eax,%edx
 8048f08:	75 0f                	jne    8048f19 <phase_6+0x9b>
 8048f0a:	e8 e9 05 00 00       	call   80494f8 <explode_bomb>
 8048f0f:	b8 00 00 00 00       	mov    $0x0,%eax
 8048f14:	e9 dc 00 00 00       	jmp    8048ff5 <phase_6+0x177>
 8048f19:	83 45 b4 01          	addl   $0x1,-0x4c(%ebp)
 8048f1d:	83 7d b4 06          	cmpl   $0x6,-0x4c(%ebp)
 8048f21:	7e d5                	jle    8048ef8 <phase_6+0x7a>
 8048f23:	83 45 b0 01          	addl   $0x1,-0x50(%ebp)
 8048f27:	83 7d b0 06          	cmpl   $0x6,-0x50(%ebp)
 8048f2b:	7e 9a                	jle    8048ec7 <phase_6+0x49>
 8048f2d:	c7 45 b0 00 00 00 00 	movl   $0x0,-0x50(%ebp)
 8048f34:	eb 36                	jmp    8048f6c <phase_6+0xee>
 8048f36:	8b 45 b8             	mov    -0x48(%ebp),%eax
 8048f39:	89 45 ac             	mov    %eax,-0x54(%ebp)
 8048f3c:	c7 45 b4 01 00 00 00 	movl   $0x1,-0x4c(%ebp)
 8048f43:	eb 0d                	jmp    8048f52 <phase_6+0xd4>
 8048f45:	8b 45 ac             	mov    -0x54(%ebp),%eax
 8048f48:	8b 40 08             	mov    0x8(%eax),%eax
 8048f4b:	89 45 ac             	mov    %eax,-0x54(%ebp)
 8048f4e:	83 45 b4 01          	addl   $0x1,-0x4c(%ebp)
 8048f52:	8b 45 b0             	mov    -0x50(%ebp),%eax
 8048f55:	8b 44 85 bc          	mov    -0x44(%ebp,%eax,4),%eax
 8048f59:	39 45 b4             	cmp    %eax,-0x4c(%ebp)
 8048f5c:	7c e7                	jl     8048f45 <phase_6+0xc7>
 8048f5e:	8b 45 b0             	mov    -0x50(%ebp),%eax
 8048f61:	8b 55 ac             	mov    -0x54(%ebp),%edx
 8048f64:	89 54 85 d8          	mov    %edx,-0x28(%ebp,%eax,4)
 8048f68:	83 45 b0 01          	addl   $0x1,-0x50(%ebp)
 8048f6c:	83 7d b0 06          	cmpl   $0x6,-0x50(%ebp)
 8048f70:	7e c4                	jle    8048f36 <phase_6+0xb8>
 8048f72:	8b 45 d8             	mov    -0x28(%ebp),%eax
 8048f75:	89 45 b8             	mov    %eax,-0x48(%ebp)
 8048f78:	8b 45 b8             	mov    -0x48(%ebp),%eax
 8048f7b:	89 45 ac             	mov    %eax,-0x54(%ebp)
 8048f7e:	c7 45 b0 01 00 00 00 	movl   $0x1,-0x50(%ebp)
 8048f85:	eb 1a                	jmp    8048fa1 <phase_6+0x123>
 8048f87:	8b 45 b0             	mov    -0x50(%ebp),%eax
 8048f8a:	8b 54 85 d8          	mov    -0x28(%ebp,%eax,4),%edx
 8048f8e:	8b 45 ac             	mov    -0x54(%ebp),%eax
 8048f91:	89 50 08             	mov    %edx,0x8(%eax)
 8048f94:	8b 45 ac             	mov    -0x54(%ebp),%eax
 8048f97:	8b 40 08             	mov    0x8(%eax),%eax
 8048f9a:	89 45 ac             	mov    %eax,-0x54(%ebp)
 8048f9d:	83 45 b0 01          	addl   $0x1,-0x50(%ebp)
 8048fa1:	83 7d b0 06          	cmpl   $0x6,-0x50(%ebp)
 8048fa5:	7e e0                	jle    8048f87 <phase_6+0x109>
 8048fa7:	8b 45 ac             	mov    -0x54(%ebp),%eax
 8048faa:	c7 40 08 00 00 00 00 	movl   $0x0,0x8(%eax)
 8048fb1:	8b 45 b8             	mov    -0x48(%ebp),%eax
 8048fb4:	89 45 ac             	mov    %eax,-0x54(%ebp)
 8048fb7:	c7 45 b0 00 00 00 00 	movl   $0x0,-0x50(%ebp)
 8048fbe:	eb 2a                	jmp    8048fea <phase_6+0x16c>
 8048fc0:	8b 45 ac             	mov    -0x54(%ebp),%eax
 8048fc3:	8b 10                	mov    (%eax),%edx
 8048fc5:	8b 45 ac             	mov    -0x54(%ebp),%eax
 8048fc8:	8b 40 08             	mov    0x8(%eax),%eax
 8048fcb:	8b 00                	mov    (%eax),%eax
 8048fcd:	39 c2                	cmp    %eax,%edx
 8048fcf:	7e 0c                	jle    8048fdd <phase_6+0x15f>
 8048fd1:	e8 22 05 00 00       	call   80494f8 <explode_bomb>
 8048fd6:	b8 00 00 00 00       	mov    $0x0,%eax
 8048fdb:	eb 18                	jmp    8048ff5 <phase_6+0x177>
 8048fdd:	8b 45 ac             	mov    -0x54(%ebp),%eax
 8048fe0:	8b 40 08             	mov    0x8(%eax),%eax
 8048fe3:	89 45 ac             	mov    %eax,-0x54(%ebp)
 8048fe6:	83 45 b0 01          	addl   $0x1,-0x50(%ebp)
 8048fea:	83 7d b0 05          	cmpl   $0x5,-0x50(%ebp)
 8048fee:	7e d0                	jle    8048fc0 <phase_6+0x142>
 8048ff0:	b8 01 00 00 00       	mov    $0x1,%eax
 8048ff5:	8b 4d f4             	mov    -0xc(%ebp),%ecx
 8048ff8:	65 33 0d 14 00 00 00 	xor    %gs:0x14,%ecx
 8048fff:	74 05                	je     8049006 <phase_6+0x188>
 8049001:	e8 ca f5 ff ff       	call   80485d0 <__stack_chk_fail@plt>
 8049006:	c9                   	leave
 8049007:	c3                   	ret

08049008 <fun7>:
 8049008:	55                   	push   %ebp
 8049009:	89 e5                	mov    %esp,%ebp
 804900b:	83 ec 08             	sub    $0x8,%esp
 804900e:	83 7d 08 00          	cmpl   $0x0,0x8(%ebp)
 8049012:	75 07                	jne    804901b <fun7+0x13>
 8049014:	b8 ff ff ff ff       	mov    $0xffffffff,%eax
 8049019:	eb 4e                	jmp    8049069 <fun7+0x61>
 804901b:	8b 45 08             	mov    0x8(%ebp),%eax
 804901e:	8b 00                	mov    (%eax),%eax
 8049020:	39 45 0c             	cmp    %eax,0xc(%ebp)
 8049023:	7d 19                	jge    804903e <fun7+0x36>
 8049025:	8b 45 08             	mov    0x8(%ebp),%eax
 8049028:	8b 40 04             	mov    0x4(%eax),%eax
 804902b:	83 ec 08             	sub    $0x8,%esp
 804902e:	ff 75 0c             	push   0xc(%ebp)
 8049031:	50                   	push   %eax
 8049032:	e8 d1 ff ff ff       	call   8049008 <fun7>
 8049037:	83 c4 10             	add    $0x10,%esp
 804903a:	01 c0                	add    %eax,%eax
 804903c:	eb 2b                	jmp    8049069 <fun7+0x61>
 804903e:	8b 45 08             	mov    0x8(%ebp),%eax
 8049041:	8b 00                	mov    (%eax),%eax
 8049043:	39 45 0c             	cmp    %eax,0xc(%ebp)
 8049046:	75 07                	jne    804904f <fun7+0x47>
 8049048:	b8 00 00 00 00       	mov    $0x0,%eax
 804904d:	eb 1a                	jmp    8049069 <fun7+0x61>
 804904f:	8b 45 08             	mov    0x8(%ebp),%eax
 8049052:	8b 40 08             	mov    0x8(%eax),%eax
 8049055:	83 ec 08             	sub    $0x8,%esp
 8049058:	ff 75 0c             	push   0xc(%ebp)
 804905b:	50                   	push   %eax
 804905c:	e8 a7 ff ff ff       	call   8049008 <fun7>
 8049061:	83 c4 10             	add    $0x10,%esp
 8049064:	01 c0                	add    %eax,%eax
 8049066:	83 c0 01             	add    $0x1,%eax
 8049069:	c9                   	leave
 804906a:	c3                   	ret

0804906b <secret_phase>:
 804906b:	55                   	push   %ebp
 804906c:	89 e5                	mov    %esp,%ebp
 804906e:	83 ec 18             	sub    $0x18,%esp
 8049071:	e8 3f 03 00 00       	call   80493b5 <read_line>
 8049076:	89 45 ec             	mov    %eax,-0x14(%ebp)
 8049079:	83 ec 0c             	sub    $0xc,%esp
 804907c:	ff 75 ec             	push   -0x14(%ebp)
 804907f:	e8 dc f5 ff ff       	call   8048660 <atoi@plt>
 8049084:	83 c4 10             	add    $0x10,%esp
 8049087:	89 45 f0             	mov    %eax,-0x10(%ebp)
 804908a:	83 7d f0 00          	cmpl   $0x0,-0x10(%ebp)
 804908e:	7e 09                	jle    8049099 <secret_phase+0x2e>
 8049090:	81 7d f0 e9 03 00 00 	cmpl   $0x3e9,-0x10(%ebp)
 8049097:	7e 0c                	jle    80490a5 <secret_phase+0x3a>
 8049099:	e8 5a 04 00 00       	call   80494f8 <explode_bomb>
 804909e:	b8 00 00 00 00       	mov    $0x0,%eax
 80490a3:	eb 42                	jmp    80490e7 <secret_phase+0x7c>
 80490a5:	83 ec 08             	sub    $0x8,%esp
 80490a8:	ff 75 f0             	push   -0x10(%ebp)
 80490ab:	68 34 c2 04 08       	push   $0x804c234
 80490b0:	e8 53 ff ff ff       	call   8049008 <fun7>
 80490b5:	83 c4 10             	add    $0x10,%esp
 80490b8:	89 45 f4             	mov    %eax,-0xc(%ebp)
 80490bb:	83 7d f4 07          	cmpl   $0x7,-0xc(%ebp)
 80490bf:	74 0c                	je     80490cd <secret_phase+0x62>
 80490c1:	e8 32 04 00 00       	call   80494f8 <explode_bomb>
 80490c6:	b8 00 00 00 00       	mov    $0x0,%eax
 80490cb:	eb 1a                	jmp    80490e7 <secret_phase+0x7c>
 80490cd:	83 ec 0c             	sub    $0xc,%esp
 80490d0:	68 88 98 04 08       	push   $0x8049888
 80490d5:	e8 16 f5 ff ff       	call   80485f0 <puts@plt>
 80490da:	83 c4 10             	add    $0x10,%esp
 80490dd:	e8 3f 04 00 00       	call   8049521 <phase_defused>
 80490e2:	b8 01 00 00 00       	mov    $0x1,%eax
 80490e7:	c9                   	leave
 80490e8:	c3                   	ret

080490e9 <sig_handler>:
 80490e9:	55                   	push   %ebp
 80490ea:	89 e5                	mov    %esp,%ebp
 80490ec:	83 ec 08             	sub    $0x8,%esp
 80490ef:	83 ec 0c             	sub    $0xc,%esp
 80490f2:	68 b0 98 04 08       	push   $0x80498b0
 80490f7:	e8 f4 f4 ff ff       	call   80485f0 <puts@plt>
 80490fc:	83 c4 10             	add    $0x10,%esp
 80490ff:	83 ec 0c             	sub    $0xc,%esp
 8049102:	6a 03                	push   $0x3
 8049104:	e8 b7 f4 ff ff       	call   80485c0 <sleep@plt>
 8049109:	83 c4 10             	add    $0x10,%esp
 804910c:	83 ec 0c             	sub    $0xc,%esp
 804910f:	68 e8 98 04 08       	push   $0x80498e8
 8049114:	e8 67 f4 ff ff       	call   8048580 <printf@plt>
 8049119:	83 c4 10             	add    $0x10,%esp
 804911c:	a1 84 c2 04 08       	mov    0x804c284,%eax
 8049121:	83 ec 0c             	sub    $0xc,%esp
 8049124:	50                   	push   %eax
 8049125:	e8 66 f4 ff ff       	call   8048590 <fflush@plt>
 804912a:	83 c4 10             	add    $0x10,%esp
 804912d:	83 ec 0c             	sub    $0xc,%esp
 8049130:	6a 01                	push   $0x1
 8049132:	e8 89 f4 ff ff       	call   80485c0 <sleep@plt>
 8049137:	83 c4 10             	add    $0x10,%esp
 804913a:	83 ec 0c             	sub    $0xc,%esp
 804913d:	68 f0 98 04 08       	push   $0x80498f0
 8049142:	e8 a9 f4 ff ff       	call   80485f0 <puts@plt>
 8049147:	83 c4 10             	add    $0x10,%esp
 804914a:	83 ec 0c             	sub    $0xc,%esp
 804914d:	6a 10                	push   $0x10
 804914f:	e8 ac f4 ff ff       	call   8048600 <exit@plt>

08049154 <invalid_phase>:
 8049154:	55                   	push   %ebp
 8049155:	89 e5                	mov    %esp,%ebp
 8049157:	83 ec 08             	sub    $0x8,%esp
 804915a:	83 ec 08             	sub    $0x8,%esp
 804915d:	ff 75 08             	push   0x8(%ebp)
 8049160:	68 f8 98 04 08       	push   $0x80498f8
 8049165:	e8 16 f4 ff ff       	call   8048580 <printf@plt>
 804916a:	83 c4 10             	add    $0x10,%esp
 804916d:	83 ec 0c             	sub    $0xc,%esp
 8049170:	6a 08                	push   $0x8
 8049172:	e8 89 f4 ff ff       	call   8048600 <exit@plt>

08049177 <read_six_numbers>:
 8049177:	55                   	push   %ebp
 8049178:	89 e5                	mov    %esp,%ebp
 804917a:	56                   	push   %esi
 804917b:	53                   	push   %ebx
 804917c:	83 ec 10             	sub    $0x10,%esp
 804917f:	8b 45 0c             	mov    0xc(%ebp),%eax
 8049182:	8d 70 14             	lea    0x14(%eax),%esi
 8049185:	8b 45 0c             	mov    0xc(%ebp),%eax
 8049188:	8d 58 10             	lea    0x10(%eax),%ebx
 804918b:	8b 45 0c             	mov    0xc(%ebp),%eax
 804918e:	8d 48 0c             	lea    0xc(%eax),%ecx
 8049191:	8b 45 0c             	mov    0xc(%ebp),%eax
 8049194:	8d 50 08             	lea    0x8(%eax),%edx
 8049197:	8b 45 0c             	mov    0xc(%ebp),%eax
 804919a:	83 c0 04             	add    $0x4,%eax
 804919d:	56                   	push   %esi
 804919e:	53                   	push   %ebx
 804919f:	51                   	push   %ecx
 80491a0:	52                   	push   %edx
 80491a1:	50                   	push   %eax
 80491a2:	ff 75 0c             	push   0xc(%ebp)
 80491a5:	68 09 99 04 08       	push   $0x8049909
 80491aa:	ff 75 08             	push   0x8(%ebp)
 80491ad:	e8 7e f4 ff ff       	call   8048630 <__isoc99_sscanf@plt>
 80491b2:	83 c4 20             	add    $0x20,%esp
 80491b5:	89 45 f4             	mov    %eax,-0xc(%ebp)
 80491b8:	83 7d f4 05          	cmpl   $0x5,-0xc(%ebp)
 80491bc:	7f 0c                	jg     80491ca <read_six_numbers+0x53>
 80491be:	e8 35 03 00 00       	call   80494f8 <explode_bomb>
 80491c3:	b8 00 00 00 00       	mov    $0x0,%eax
 80491c8:	eb 05                	jmp    80491cf <read_six_numbers+0x58>
 80491ca:	b8 01 00 00 00       	mov    $0x1,%eax
 80491cf:	8d 65 f8             	lea    -0x8(%ebp),%esp
 80491d2:	5b                   	pop    %ebx
 80491d3:	5e                   	pop    %esi
 80491d4:	5d                   	pop    %ebp
 80491d5:	c3                   	ret

080491d6 <read_n_numbers>:
 80491d6:	55                   	push   %ebp
 80491d7:	89 e5                	mov    %esp,%ebp
 80491d9:	83 ec 18             	sub    $0x18,%esp
 80491dc:	c7 45 f4 00 00 00 00 	movl   $0x0,-0xc(%ebp)
 80491e3:	eb 70                	jmp    8049255 <read_n_numbers+0x7f>
 80491e5:	83 7d f4 00          	cmpl   $0x0,-0xc(%ebp)
 80491e9:	75 18                	jne    8049203 <read_n_numbers+0x2d>
 80491eb:	83 ec 08             	sub    $0x8,%esp
 80491ee:	68 1b 99 04 08       	push   $0x804991b
 80491f3:	ff 75 08             	push   0x8(%ebp)
 80491f6:	e8 55 f4 ff ff       	call   8048650 <strtok@plt>
 80491fb:	83 c4 10             	add    $0x10,%esp
 80491fe:	89 45 f0             	mov    %eax,-0x10(%ebp)
 8049201:	eb 15                	jmp    8049218 <read_n_numbers+0x42>
 8049203:	83 ec 08             	sub    $0x8,%esp
 8049206:	68 1b 99 04 08       	push   $0x804991b
 804920b:	6a 00                	push   $0x0
 804920d:	e8 3e f4 ff ff       	call   8048650 <strtok@plt>
 8049212:	83 c4 10             	add    $0x10,%esp
 8049215:	89 45 f0             	mov    %eax,-0x10(%ebp)
 8049218:	83 7d f0 00          	cmpl   $0x0,-0x10(%ebp)
 804921c:	74 27                	je     8049245 <read_n_numbers+0x6f>
 804921e:	8b 45 f4             	mov    -0xc(%ebp),%eax
 8049221:	8d 14 85 00 00 00 00 	lea    0x0(,%eax,4),%edx
 8049228:	8b 45 0c             	mov    0xc(%ebp),%eax
 804922b:	01 d0                	add    %edx,%eax
 804922d:	83 ec 04             	sub    $0x4,%esp
 8049230:	50                   	push   %eax
 8049231:	68 1f 99 04 08       	push   $0x804991f
 8049236:	ff 75 f0             	push   -0x10(%ebp)
 8049239:	e8 f2 f3 ff ff       	call   8048630 <__isoc99_sscanf@plt>
 804923e:	83 c4 10             	add    $0x10,%esp
 8049241:	85 c0                	test   %eax,%eax
 8049243:	7f 0c                	jg     8049251 <read_n_numbers+0x7b>
 8049245:	e8 ae 02 00 00       	call   80494f8 <explode_bomb>
 804924a:	b8 00 00 00 00       	mov    $0x0,%eax
 804924f:	eb 11                	jmp    8049262 <read_n_numbers+0x8c>
 8049251:	83 45 f4 01          	addl   $0x1,-0xc(%ebp)
 8049255:	8b 45 f4             	mov    -0xc(%ebp),%eax
 8049258:	3b 45 10             	cmp    0x10(%ebp),%eax
 804925b:	7c 88                	jl     80491e5 <read_n_numbers+0xf>
 804925d:	b8 01 00 00 00       	mov    $0x1,%eax
 8049262:	c9                   	leave
 8049263:	c3                   	ret

08049264 <string_length>:
 8049264:	55                   	push   %ebp
 8049265:	89 e5                	mov    %esp,%ebp
 8049267:	83 ec 10             	sub    $0x10,%esp
 804926a:	8b 45 08             	mov    0x8(%ebp),%eax
 804926d:	89 45 fc             	mov    %eax,-0x4(%ebp)
 8049270:	c7 45 f8 00 00 00 00 	movl   $0x0,-0x8(%ebp)
 8049277:	eb 08                	jmp    8049281 <string_length+0x1d>
 8049279:	83 45 fc 01          	addl   $0x1,-0x4(%ebp)
 804927d:	83 45 f8 01          	addl   $0x1,-0x8(%ebp)
 8049281:	8b 45 fc             	mov    -0x4(%ebp),%eax
 8049284:	0f b6 00             	movzbl (%eax),%eax
 8049287:	84 c0                	test   %al,%al
 8049289:	75 ee                	jne    8049279 <string_length+0x15>
 804928b:	8b 45 f8             	mov    -0x8(%ebp),%eax
 804928e:	c9                   	leave
 804928f:	c3                   	ret

08049290 <strings_not_equal>:
 8049290:	55                   	push   %ebp
 8049291:	89 e5                	mov    %esp,%ebp
 8049293:	53                   	push   %ebx
 8049294:	83 ec 10             	sub    $0x10,%esp
 8049297:	ff 75 08             	push   0x8(%ebp)
 804929a:	e8 c5 ff ff ff       	call   8049264 <string_length>
 804929f:	83 c4 04             	add    $0x4,%esp
 80492a2:	89 c3                	mov    %eax,%ebx
 80492a4:	ff 75 0c             	push   0xc(%ebp)
 80492a7:	e8 b8 ff ff ff       	call   8049264 <string_length>
 80492ac:	83 c4 04             	add    $0x4,%esp
 80492af:	39 c3                	cmp    %eax,%ebx
 80492b1:	74 07                	je     80492ba <strings_not_equal+0x2a>
 80492b3:	b8 01 00 00 00       	mov    $0x1,%eax
 80492b8:	eb 3c                	jmp    80492f6 <strings_not_equal+0x66>
 80492ba:	8b 45 08             	mov    0x8(%ebp),%eax
 80492bd:	89 45 f4             	mov    %eax,-0xc(%ebp)
 80492c0:	8b 45 0c             	mov    0xc(%ebp),%eax
 80492c3:	89 45 f8             	mov    %eax,-0x8(%ebp)
 80492c6:	eb 1f                	jmp    80492e7 <strings_not_equal+0x57>
 80492c8:	8b 45 f4             	mov    -0xc(%ebp),%eax
 80492cb:	0f b6 10             	movzbl (%eax),%edx
 80492ce:	8b 45 f8             	mov    -0x8(%ebp),%eax
 80492d1:	0f b6 00             	movzbl (%eax),%eax
 80492d4:	38 c2                	cmp    %al,%dl
 80492d6:	74 07                	je     80492df <strings_not_equal+0x4f>
 80492d8:	b8 01 00 00 00       	mov    $0x1,%eax
 80492dd:	eb 17                	jmp    80492f6 <strings_not_equal+0x66>
 80492df:	83 45 f4 01          	addl   $0x1,-0xc(%ebp)
 80492e3:	83 45 f8 01          	addl   $0x1,-0x8(%ebp)
 80492e7:	8b 45 f4             	mov    -0xc(%ebp),%eax
 80492ea:	0f b6 00             	movzbl (%eax),%eax
 80492ed:	84 c0                	test   %al,%al
 80492ef:	75 d7                	jne    80492c8 <strings_not_equal+0x38>
 80492f1:	b8 00 00 00 00       	mov    $0x0,%eax
 80492f6:	8b 5d fc             	mov    -0x4(%ebp),%ebx
 80492f9:	c9                   	leave
 80492fa:	c3                   	ret

080492fb <initialize_bomb>:
 80492fb:	55                   	push   %ebp
 80492fc:	89 e5                	mov    %esp,%ebp
 80492fe:	83 ec 08             	sub    $0x8,%esp
 8049301:	83 ec 08             	sub    $0x8,%esp
 8049304:	68 e9 90 04 08       	push   $0x80490e9
 8049309:	6a 02                	push   $0x2
 804930b:	e8 a0 f2 ff ff       	call   80485b0 <signal@plt>
 8049310:	83 c4 10             	add    $0x10,%esp
 8049313:	90                   	nop
 8049314:	c9                   	leave
 8049315:	c3                   	ret

08049316 <initialize_bomb_solve>:
 8049316:	55                   	push   %ebp
 8049317:	89 e5                	mov    %esp,%ebp
 8049319:	90                   	nop
 804931a:	5d                   	pop    %ebp
 804931b:	c3                   	ret

0804931c <blank_line>:
 804931c:	55                   	push   %ebp
 804931d:	89 e5                	mov    %esp,%ebp
 804931f:	83 ec 08             	sub    $0x8,%esp
 8049322:	eb 30                	jmp    8049354 <blank_line+0x38>
 8049324:	e8 47 f3 ff ff       	call   8048670 <__ctype_b_loc@plt>
 8049329:	8b 08                	mov    (%eax),%ecx
 804932b:	8b 45 08             	mov    0x8(%ebp),%eax
 804932e:	8d 50 01             	lea    0x1(%eax),%edx
 8049331:	89 55 08             	mov    %edx,0x8(%ebp)
 8049334:	0f b6 00             	movzbl (%eax),%eax
 8049337:	0f be c0             	movsbl %al,%eax
 804933a:	01 c0                	add    %eax,%eax
 804933c:	01 c8                	add    %ecx,%eax
 804933e:	0f b7 00             	movzwl (%eax),%eax
 8049341:	0f b7 c0             	movzwl %ax,%eax
 8049344:	25 00 20 00 00       	and    $0x2000,%eax
 8049349:	85 c0                	test   %eax,%eax
 804934b:	75 07                	jne    8049354 <blank_line+0x38>
 804934d:	b8 00 00 00 00       	mov    $0x0,%eax
 8049352:	eb 0f                	jmp    8049363 <blank_line+0x47>
 8049354:	8b 45 08             	mov    0x8(%ebp),%eax
 8049357:	0f b6 00             	movzbl (%eax),%eax
 804935a:	84 c0                	test   %al,%al
 804935c:	75 c6                	jne    8049324 <blank_line+0x8>
 804935e:	b8 01 00 00 00       	mov    $0x1,%eax
 8049363:	c9                   	leave
 8049364:	c3                   	ret

08049365 <skip>:
 8049365:	55                   	push   %ebp
 8049366:	89 e5                	mov    %esp,%ebp
 8049368:	83 ec 18             	sub    $0x18,%esp
 804936b:	8b 0d 90 c2 04 08    	mov    0x804c290,%ecx
 8049371:	8b 15 8c c2 04 08    	mov    0x804c28c,%edx
 8049377:	89 d0                	mov    %edx,%eax
 8049379:	c1 e0 02             	shl    $0x2,%eax
 804937c:	01 d0                	add    %edx,%eax
 804937e:	c1 e0 04             	shl    $0x4,%eax
 8049381:	05 a0 c2 04 08       	add    $0x804c2a0,%eax
 8049386:	83 ec 04             	sub    $0x4,%esp
 8049389:	51                   	push   %ecx
 804938a:	6a 50                	push   $0x50
 804938c:	50                   	push   %eax
 804938d:	e8 0e f2 ff ff       	call   80485a0 <fgets@plt>
 8049392:	83 c4 10             	add    $0x10,%esp
 8049395:	89 45 f4             	mov    %eax,-0xc(%ebp)
 8049398:	83 7d f4 00          	cmpl   $0x0,-0xc(%ebp)
 804939c:	74 12                	je     80493b0 <skip+0x4b>
 804939e:	83 ec 0c             	sub    $0xc,%esp
 80493a1:	ff 75 f4             	push   -0xc(%ebp)
 80493a4:	e8 73 ff ff ff       	call   804931c <blank_line>
 80493a9:	83 c4 10             	add    $0x10,%esp
 80493ac:	85 c0                	test   %eax,%eax
 80493ae:	75 bb                	jne    804936b <skip+0x6>
 80493b0:	8b 45 f4             	mov    -0xc(%ebp),%eax
 80493b3:	c9                   	leave
 80493b4:	c3                   	ret

080493b5 <read_line>:
 80493b5:	55                   	push   %ebp
 80493b6:	89 e5                	mov    %esp,%ebp
 80493b8:	83 ec 18             	sub    $0x18,%esp
 80493bb:	e8 a5 ff ff ff       	call   8049365 <skip>
 80493c0:	89 45 f0             	mov    %eax,-0x10(%ebp)
 80493c3:	83 7d f0 00          	cmpl   $0x0,-0x10(%ebp)
 80493c7:	75 79                	jne    8049442 <read_line+0x8d>
 80493c9:	8b 15 90 c2 04 08    	mov    0x804c290,%edx
 80493cf:	a1 80 c2 04 08       	mov    0x804c280,%eax
 80493d4:	39 c2                	cmp    %eax,%edx
 80493d6:	75 1a                	jne    80493f2 <read_line+0x3d>
 80493d8:	83 ec 0c             	sub    $0xc,%esp
 80493db:	68 22 99 04 08       	push   $0x8049922
 80493e0:	e8 0b f2 ff ff       	call   80485f0 <puts@plt>
 80493e5:	83 c4 10             	add    $0x10,%esp
 80493e8:	83 ec 0c             	sub    $0xc,%esp
 80493eb:	6a 08                	push   $0x8
 80493ed:	e8 0e f2 ff ff       	call   8048600 <exit@plt>
 80493f2:	83 ec 0c             	sub    $0xc,%esp
 80493f5:	68 40 99 04 08       	push   $0x8049940
 80493fa:	e8 e1 f1 ff ff       	call   80485e0 <getenv@plt>
 80493ff:	83 c4 10             	add    $0x10,%esp
 8049402:	85 c0                	test   %eax,%eax
 8049404:	74 0a                	je     8049410 <read_line+0x5b>
 8049406:	83 ec 0c             	sub    $0xc,%esp
 8049409:	6a 00                	push   $0x0
 804940b:	e8 f0 f1 ff ff       	call   8048600 <exit@plt>
 8049410:	a1 80 c2 04 08       	mov    0x804c280,%eax
 8049415:	a3 90 c2 04 08       	mov    %eax,0x804c290
 804941a:	e8 46 ff ff ff       	call   8049365 <skip>
 804941f:	89 45 f0             	mov    %eax,-0x10(%ebp)
 8049422:	83 7d f0 00          	cmpl   $0x0,-0x10(%ebp)
 8049426:	75 1a                	jne    8049442 <read_line+0x8d>
 8049428:	83 ec 0c             	sub    $0xc,%esp
 804942b:	68 22 99 04 08       	push   $0x8049922
 8049430:	e8 bb f1 ff ff       	call   80485f0 <puts@plt>
 8049435:	83 c4 10             	add    $0x10,%esp
 8049438:	83 ec 0c             	sub    $0xc,%esp
 804943b:	6a 00                	push   $0x0
 804943d:	e8 be f1 ff ff       	call   8048600 <exit@plt>
 8049442:	8b 15 8c c2 04 08    	mov    0x804c28c,%edx
 8049448:	89 d0                	mov    %edx,%eax
 804944a:	c1 e0 02             	shl    $0x2,%eax
 804944d:	01 d0                	add    %edx,%eax
 804944f:	c1 e0 04             	shl    $0x4,%eax
 8049452:	05 a0 c2 04 08       	add    $0x804c2a0,%eax
 8049457:	83 ec 0c             	sub    $0xc,%esp
 804945a:	50                   	push   %eax
 804945b:	e8 b0 f1 ff ff       	call   8048610 <strlen@plt>
 8049460:	83 c4 10             	add    $0x10,%esp
 8049463:	89 45 f4             	mov    %eax,-0xc(%ebp)
 8049466:	83 7d f4 4e          	cmpl   $0x4e,-0xc(%ebp)
 804946a:	7e 4d                	jle    80494b9 <read_line+0x104>
 804946c:	83 ec 0c             	sub    $0xc,%esp
 804946f:	68 4b 99 04 08       	push   $0x804994b
 8049474:	e8 77 f1 ff ff       	call   80485f0 <puts@plt>
 8049479:	83 c4 10             	add    $0x10,%esp
 804947c:	8b 15 8c c2 04 08    	mov    0x804c28c,%edx
 8049482:	8d 42 01             	lea    0x1(%edx),%eax
 8049485:	a3 8c c2 04 08       	mov    %eax,0x804c28c
 804948a:	89 d0                	mov    %edx,%eax
 804948c:	c1 e0 02             	shl    $0x2,%eax
 804948f:	01 d0                	add    %edx,%eax
 8049491:	c1 e0 04             	shl    $0x4,%eax
 8049494:	05 a0 c2 04 08       	add    $0x804c2a0,%eax
 8049499:	c7 00 2a 2a 2a 74    	movl   $0x742a2a2a,(%eax)
 804949f:	c7 40 04 72 75 6e 63 	movl   $0x636e7572,0x4(%eax)
 80494a6:	c7 40 08 61 74 65 64 	movl   $0x64657461,0x8(%eax)
 80494ad:	c7 40 0c 2a 2a 2a 00 	movl   $0x2a2a2a,0xc(%eax)
 80494b4:	e8 3f 00 00 00       	call   80494f8 <explode_bomb>
 80494b9:	8b 15 8c c2 04 08    	mov    0x804c28c,%edx
 80494bf:	8b 45 f4             	mov    -0xc(%ebp),%eax
 80494c2:	8d 48 ff             	lea    -0x1(%eax),%ecx
 80494c5:	89 d0                	mov    %edx,%eax
 80494c7:	c1 e0 02             	shl    $0x2,%eax
 80494ca:	01 d0                	add    %edx,%eax
 80494cc:	c1 e0 04             	shl    $0x4,%eax
 80494cf:	01 c8                	add    %ecx,%eax
 80494d1:	05 a0 c2 04 08       	add    $0x804c2a0,%eax
 80494d6:	c6 00 00             	movb   $0x0,(%eax)
 80494d9:	8b 15 8c c2 04 08    	mov    0x804c28c,%edx
 80494df:	8d 42 01             	lea    0x1(%edx),%eax
 80494e2:	a3 8c c2 04 08       	mov    %eax,0x804c28c
 80494e7:	89 d0                	mov    %edx,%eax
 80494e9:	c1 e0 02             	shl    $0x2,%eax
 80494ec:	01 d0                	add    %edx,%eax
 80494ee:	c1 e0 04             	shl    $0x4,%eax
 80494f1:	05 a0 c2 04 08       	add    $0x804c2a0,%eax
 80494f6:	c9                   	leave
 80494f7:	c3                   	ret

080494f8 <explode_bomb>:
 80494f8:	55                   	push   %ebp
 80494f9:	89 e5                	mov    %esp,%ebp
 80494fb:	83 ec 08             	sub    $0x8,%esp
 80494fe:	83 ec 0c             	sub    $0xc,%esp
 8049501:	68 66 99 04 08       	push   $0x8049966
 8049506:	e8 e5 f0 ff ff       	call   80485f0 <puts@plt>
 804950b:	83 c4 10             	add    $0x10,%esp
 804950e:	83 ec 0c             	sub    $0xc,%esp
 8049511:	68 6f 99 04 08       	push   $0x804996f
 8049516:	e8 d5 f0 ff ff       	call   80485f0 <puts@plt>
 804951b:	83 c4 10             	add    $0x10,%esp
 804951e:	90                   	nop
 804951f:	c9                   	leave
 8049520:	c3                   	ret

08049521 <phase_defused>:
 8049521:	55                   	push   %ebp
 8049522:	89 e5                	mov    %esp,%ebp
 8049524:	83 ec 68             	sub    $0x68,%esp
 8049527:	65 a1 14 00 00 00    	mov    %gs:0x14,%eax
 804952d:	89 45 f4             	mov    %eax,-0xc(%ebp)
 8049530:	31 c0                	xor    %eax,%eax
 8049532:	a1 8c c2 04 08       	mov    0x804c28c,%eax
 8049537:	83 f8 07             	cmp    $0x7,%eax
 804953a:	75 77                	jne    80495b3 <phase_defused+0x92>
 804953c:	83 ec 0c             	sub    $0xc,%esp
 804953f:	8d 45 a4             	lea    -0x5c(%ebp),%eax
 8049542:	50                   	push   %eax
 8049543:	8d 45 9c             	lea    -0x64(%ebp),%eax
 8049546:	50                   	push   %eax
 8049547:	8d 45 98             	lea    -0x68(%ebp),%eax
 804954a:	50                   	push   %eax
 804954b:	68 86 99 04 08       	push   $0x8049986
 8049550:	68 e0 c3 04 08       	push   $0x804c3e0
 8049555:	e8 d6 f0 ff ff       	call   8048630 <__isoc99_sscanf@plt>
 804955a:	83 c4 20             	add    $0x20,%esp
 804955d:	89 45 a0             	mov    %eax,-0x60(%ebp)
 8049560:	83 7d a0 03          	cmpl   $0x3,-0x60(%ebp)
 8049564:	75 3d                	jne    80495a3 <phase_defused+0x82>
 8049566:	83 ec 08             	sub    $0x8,%esp
 8049569:	68 8f 99 04 08       	push   $0x804998f
 804956e:	8d 45 a4             	lea    -0x5c(%ebp),%eax
 8049571:	50                   	push   %eax
 8049572:	e8 19 fd ff ff       	call   8049290 <strings_not_equal>
 8049577:	83 c4 10             	add    $0x10,%esp
 804957a:	85 c0                	test   %eax,%eax
 804957c:	75 25                	jne    80495a3 <phase_defused+0x82>
 804957e:	83 ec 0c             	sub    $0xc,%esp
 8049581:	68 98 99 04 08       	push   $0x8049998
 8049586:	e8 65 f0 ff ff       	call   80485f0 <puts@plt>
 804958b:	83 c4 10             	add    $0x10,%esp
 804958e:	83 ec 0c             	sub    $0xc,%esp
 8049591:	68 c0 99 04 08       	push   $0x80499c0
 8049596:	e8 55 f0 ff ff       	call   80485f0 <puts@plt>
 804959b:	83 c4 10             	add    $0x10,%esp
 804959e:	e8 c8 fa ff ff       	call   804906b <secret_phase>
 80495a3:	83 ec 0c             	sub    $0xc,%esp
 80495a6:	68 f8 99 04 08       	push   $0x80499f8
 80495ab:	e8 40 f0 ff ff       	call   80485f0 <puts@plt>
 80495b0:	83 c4 10             	add    $0x10,%esp
 80495b3:	90                   	nop
 80495b4:	8b 45 f4             	mov    -0xc(%ebp),%eax
 80495b7:	65 33 05 14 00 00 00 	xor    %gs:0x14,%eax
 80495be:	74 05                	je     80495c5 <phase_defused+0xa4>
 80495c0:	e8 0b f0 ff ff       	call   80485d0 <__stack_chk_fail@plt>
 80495c5:	c9                   	leave
 80495c6:	c3                   	ret
 80495c7:	66 90                	xchg   %ax,%ax
 80495c9:	66 90                	xchg   %ax,%ax
 80495cb:	66 90                	xchg   %ax,%ax
 80495cd:	66 90                	xchg   %ax,%ax
 80495cf:	90                   	nop

080495d0 <__libc_csu_init>:
 80495d0:	55                   	push   %ebp
 80495d1:	57                   	push   %edi
 80495d2:	56                   	push   %esi
 80495d3:	53                   	push   %ebx
 80495d4:	e8 07 f1 ff ff       	call   80486e0 <__x86.get_pc_thunk.bx>
 80495d9:	81 c3 27 2a 00 00    	add    $0x2a27,%ebx
 80495df:	83 ec 0c             	sub    $0xc,%esp
 80495e2:	8b 6c 24 28          	mov    0x28(%esp),%ebp
 80495e6:	8d b3 10 ff ff ff    	lea    -0xf0(%ebx),%esi
 80495ec:	e8 4f ef ff ff       	call   8048540 <_init>
 80495f1:	8d 83 0c ff ff ff    	lea    -0xf4(%ebx),%eax
 80495f7:	29 c6                	sub    %eax,%esi
 80495f9:	c1 fe 02             	sar    $0x2,%esi
 80495fc:	85 f6                	test   %esi,%esi
 80495fe:	74 25                	je     8049625 <__libc_csu_init+0x55>
 8049600:	31 ff                	xor    %edi,%edi
 8049602:	8d b6 00 00 00 00    	lea    0x0(%esi),%esi
 8049608:	83 ec 04             	sub    $0x4,%esp
 804960b:	55                   	push   %ebp
 804960c:	ff 74 24 2c          	push   0x2c(%esp)
 8049610:	ff 74 24 2c          	push   0x2c(%esp)
 8049614:	ff 94 bb 0c ff ff ff 	call   *-0xf4(%ebx,%edi,4)
 804961b:	83 c7 01             	add    $0x1,%edi
 804961e:	83 c4 10             	add    $0x10,%esp
 8049621:	39 fe                	cmp    %edi,%esi
 8049623:	75 e3                	jne    8049608 <__libc_csu_init+0x38>
 8049625:	83 c4 0c             	add    $0xc,%esp
 8049628:	5b                   	pop    %ebx
 8049629:	5e                   	pop    %esi
 804962a:	5f                   	pop    %edi
 804962b:	5d                   	pop    %ebp
 804962c:	c3                   	ret
 804962d:	8d 76 00             	lea    0x0(%esi),%esi

08049630 <__libc_csu_fini>:
 8049630:	f3 c3                	repz ret

Disassembly of section .fini:

08049634 <_fini>:
 8049634:	53                   	push   %ebx
 8049635:	83 ec 08             	sub    $0x8,%esp
 8049638:	e8 a3 f0 ff ff       	call   80486e0 <__x86.get_pc_thunk.bx>
 804963d:	81 c3 c3 29 00 00    	add    $0x29c3,%ebx
 8049643:	83 c4 08             	add    $0x8,%esp
 8049646:	5b                   	pop    %ebx
 8049647:	c3                   	ret